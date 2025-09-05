import socket
import sqlite3
from datetime import datetime

# Constantes
HOST = '127.0.0.1'  
PORT = 5000
DB_NAME = 'mensajes.db'

def inicializar_socket():
    """
    Inicializa el socket TCP/IP y lo prepara para escuchar conexiones.
    Maneja el error si el puerto está ocupado.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")
    except OSError as e:
        print(f"Error al iniciar el socket: {e}")
        s.close()
        exit(1)
    return s

def inicializar_db():
    """
    Inicializa la base de datos SQLite, creando la tabla si no existe.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        exit(1)
    return conn

def guardar_mensaje(conn, contenido, ip_cliente):
    """
    Guarda un mensaje recibido en la base de datos con la fecha actual y la IP del cliente.
    """
    try:
        cursor = conn.cursor()
        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar el mensaje en la base de datos: {e}")

def manejar_cliente(conn, cliente_socket, addr):
    """
    Recibe mensajes del cliente y guarda cada uno en la base de datos.
    Envía una confirmación con timestamp luego de cada mensaje.
    Finaliza cuando el cliente cierra la conexión.
    """
    ip_cliente = addr[0]
    with cliente_socket:
        while True:
            try:
                data = cliente_socket.recv(1024)  # Tamaño máximo del mensaje
                if not data:
                    print(f"Conexión cerrada por {ip_cliente}")
                    break

                mensaje = data.decode('utf-8')

                # Guardar mensaje en DB
                guardar_mensaje(conn, mensaje, ip_cliente)

                # Enviar confirmación con timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                confirmacion = f"Mensaje recibido: {timestamp}"
                cliente_socket.sendall(confirmacion.encode('utf-8'))

            except Exception as e:
                print(f"Error al manejar mensaje de {ip_cliente}: {e}")
                break

def main():
    # Inicializa DB y socket
    conn = inicializar_db()
    server_socket = inicializar_socket()

    try:
        while True:
            # Acepta conexiones entrantes
            cliente_socket, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")
            manejar_cliente(conn, cliente_socket, addr)
    except KeyboardInterrupt:
        print("\nServidor cerrado manualmente.")
    finally:
        conn.close()
        server_socket.close()

if __name__ == '__main__':
    main()
