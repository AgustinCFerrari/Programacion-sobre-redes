import socket

# Configuración del servidor
HOST = "localhost"  # Escucha en localhost (máquina local)
PORT = 1234         # Puerto arbitrario (debe ser > 1024)

# Diccionario de preguntas y respuestas
respuestas = {
    "¿Cuál es la capital de Francia?": "París",
    "¿Cuántos lados tiene un cuadrado?": "4",
    "¿Qué lenguaje usamos?": "Python",
}

# Crear el socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Vincular el socket al puerto y host
    s.bind((HOST, PORT))
    # Escuchar conexiones entrantes (máx. 1 en este ejemplo)
    s.listen(1)
    print(f"Servidor escuchando en {HOST}:{PORT}...")

    # Aceptar una conexión
    conn, addr = s.accept()
    with conn:
        print(f"Conexión establecida desde {addr}")
        while True:
            # Recibir la pregunta del cliente (hasta 1024 bytes)
            pregunta = conn.recv(1024).decode("utf-8")
            if not pregunta:
                break  # Si no hay datos, cerrar conexión

            print(f"Cliente preguntó: {pregunta}")

            # Buscar la respuesta en el diccionario
            respuesta = respuestas.get(pregunta, "No sé la respuesta")

            # Enviar la respuesta al cliente
            conn.sendall(respuesta.encode("utf-8"))

    print("Conexión cerrada.")
