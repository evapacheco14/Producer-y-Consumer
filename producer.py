import socket
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 7000

def Mostrar_Menu():
    print("Seleccione una tarea:\n")
    print("1. Sumar dos números")
    print("2. Convertir una cadena a mayúsculas")
    print("3. Invertir una cadena")
    print("4. salir - Terminar las tareas")
    tarea = input("\nIngrese el número de la tarea: ")
    return tarea

def obtener_parametros(tarea):
    try:
        if tarea == "1": 
            num1 = float(input("Digite el primer número: "))
            num2 = float(input("Digite el segundo número: "))
            return [num1, num2]
        elif tarea == "2":  
            cadena = input("Digite la cadena: ")
            return [cadena]
        elif tarea == "3":  
            cadena = input("Digite la cadena a invertir: ")
            return [cadena]
        elif tarea == "4" or tarea.lower() == "salir":  
            return []
        else:
            print("Opción no válida. Intente nuevamente.")
            return None
    except Exception as e:
        print(f"Error al obtener parámetros: {e}")
        return None

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Conectado al servidor {SERVER_HOST}:{SERVER_PORT}")
    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")
        return

    try:
        while True:
            opcion = Mostrar_Menu()

            if opcion == '4' or opcion.lower() == 'salir':
                break

            parametros = obtener_parametros(opcion)
            if parametros is None:
                continue

            tarea = None
            if opcion == '1':
                tarea = "sumar"
            elif opcion == '2':
                tarea = "a_mayusculas"
            elif opcion == '3':
                tarea = "invertir_cadena"

            mensaje = json.dumps({
                "tarea": tarea,
                "parametros": parametros
            })

            client_socket.sendall(mensaje.encode())
            print(f"Tarea '{tarea}' enviada al servidor con parámetros {parametros}")

    except Exception as e:
        print(f"Error durante la ejecución: {e}")

    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
