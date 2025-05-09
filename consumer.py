import socket
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 7000

def execute_task(task, parameters):
    if task == "sumar":
        result = sum(parameters)
    elif task == "a_mayusculas":
        result = parameters[0].upper()
    elif task == "invertir_cadena":
        result = parameters[0][::-1]
    else:
        return f"Tarea '{task}' no válida"

    return result

def start_consumer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    try:
        while True:
            message = client_socket.recv(1024)

            if not message:
                break

            try:
                request = json.loads(message.decode())
                task = request.get("tarea")
                parameters = request.get("parametros")

                if task and parameters:
                    result = execute_task(task, parameters)
                    print("Resultado:", result)
                else:
                    print("Mensaje recibido no válido:", request)

            except json.JSONDecodeError as e:
                print("Error al decodificar JSON:", e)
                continue

    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    start_consumer()
