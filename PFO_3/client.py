import socket

# Función para enviar una tarea al servidor por medio de un socket TCP
def send_task(task):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Crea el socket TCP
    client.connect(('127.0.0.1', 8080))                           # Conecta al servidor en localhost y puerto 8080
    client.send(task.encode())                                    # Envía la tarea al servidor
    response = client.recv(1024).decode()                         # Recibe la respuesta del servidor
    print(f"Respuesta del servidor: {response}")                  # Imprime la respuesta recibida
    client.close()                                                # Cierra el socket

if __name__ == "__main__":
    # Bucle principal para pedir tareas al usuario hasta que escriba 'close'
    while True:
        msg = input("Ingrese la tarea (o 'close' para salir): ")  # Pide una tarea al usuario
        if msg.lower() == 'close':                                # Si el usuario escribe 'close', se termina el programa
            break
        send_task(msg)                                            # Envía la tarea al servidor
