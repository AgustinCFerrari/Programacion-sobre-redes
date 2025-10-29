import socket

def send_task(task):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    client.send(task.encode())
    response = client.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")
    client.close()

if __name__ == "__main__":
    while True:
        msg = input("Ingrese la tarea (o 'close' para salir): ")
        if msg.lower() == 'close':
            break
        send_task(msg)
