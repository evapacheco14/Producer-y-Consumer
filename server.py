import socket
import threading
import datetime


HOST = 'localhost'
PORT =  7000
LOG_FILE = 'chat_log.txt'

clients = []
clients_lock = threading.Lock()

def log_event(ip, action):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"({timestamp}) {ip} - {action}\n")

def broadcast(message, source_socket):
    with clients_lock:
        for client in clients:
            if client != source_socket:
                try:
                    client.sendall(message)
                    log_event(client.getpeername()[0], "mensaje enviado")
                except:
                    remove_client(client)

def remove_client(client):
    with clients_lock:
        if client in clients:
            ip = client.getpeername()[0]
            clients.remove(client)
            client.close()
            log_event(ip, "remover conexion")

def handle_client(client_socket, address):
    ip = address[0]
    log_event(ip, "añadir conexion")
    with clients_lock:
        clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break 
            log_event(ip, "mensaje recibido")
            broadcast(message, client_socket)
    except:
        pass
    finally:
        remove_client(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()
    except KeyboardInterrupt:
        print("Servidor detenido.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()