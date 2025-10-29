import socket
import threading
import pika

def publish_task(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_publish(exchange='', routing_key='tasks', body=message)
    connection.close()

def handle_client(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data or data.lower() == 'close':
            break
        publish_task(data)
        conn.send(b'Tarea enviada a RabbitMQ')
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("Servidor escuchando en el puerto 8080...")
    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()
