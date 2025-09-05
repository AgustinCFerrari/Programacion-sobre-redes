import socket

# Constantes
HOST = '127.0.0.1'
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Conectado al servidor en {HOST}:{PORT}")
        except ConnectionRefusedError:
            print(f"No se pudo conectar al servidor en {HOST}:{PORT}")
            return

        while True:
            mensaje = input("Ingrese mensaje (o 'salir' para terminar): ")
            if mensaje.lower() == 'salir':
                print("Finalizando conexión.")
                break
            
            try:
                # Enviar mensaje al servidor
                s.sendall(mensaje.encode('utf-8'))

                # Recibir respuesta del servidor
                data = s.recv(1024)
                print('Respuesta del servidor:', data.decode('utf-8'))
            except Exception as e:
                print(f"Error durante la comunicación con el servidor: {e}")
                break

if __name__ == '__main__':
    main()
