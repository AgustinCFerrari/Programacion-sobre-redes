import socket
import threading
import pika

# Publica la tarea recibida en la cola de RabbitMQ
def publish_task(message):
    # Conexión a RabbitMQ en la máquina local
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')  # Declara la cola 'tasks'
    channel.basic_publish(exchange='', routing_key='tasks', body=message)  # Publica el mensaje en la cola
    connection.close()  # Cierra la conexión a RabbitMQ

# Atiende un cliente a través de un socket TCP
def handle_client(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        data = conn.recv(1024).decode()  # Recibe datos del cliente
        if not data or data.lower() == 'close':  
            break
        publish_task(data)  # Publica la tarea en RabbitMQ
        conn.send(b'Tarea enviada a RabbitMQ')  # Notifica al cliente que la tarea fue enviada
    conn.close()  # Cierra la conexión con el cliente

# Inicia el servidor TCP y acepta conexiones entrantes
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))  # Escucha en todas las interfaces, puerto 8080
    server.listen(5)  # Permite hasta 5 conexiones en espera
    print("Servidor escuchando en el puerto 8080...")
    while True:
        client_socket, address = server.accept()  # Acepta conexión de cliente
        # Atiende cada cliente en un hilo independiente
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()  # Inicia el servidor TCP
