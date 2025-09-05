import threading
import time

def contar_numeros(nombre, inicio, fin): # Función que cuenta números entre inicio y fin.
    for i in range(inicio, fin + 1):
        time.sleep(1)  # Simula trabajo que tarda
        print(f"{nombre} está contando: {i}")

def main():
    # Configuración centralizada: lista de hilos con sus parámetros
    configuraciones = [
        ("Hilo 1", 1, 5),
        ("Hilo 2", 6, 10),
        ("Hilo 3", 11, 15),  # se pueden agregar más hilos
    ]

    hilos = [] # Lista para almacenar los hilos

    # Crear hilos dinámicamente
    for nombre, inicio, fin in configuraciones:
        t = threading.Thread(target=contar_numeros, args=(nombre, inicio, fin)) # Crear un hilo
        hilos.append(t) # Agregar el hilo a la lista
        t.start() # Iniciar el hilo

    # Esperar a que todos los hilos terminen
    for t in hilos:
        t.join()

    print("Hecho!")

main()
