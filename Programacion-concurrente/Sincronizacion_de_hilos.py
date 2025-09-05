import threading

def sumar(nombre, condicion, resultados):
    # Cálculo directo: 1+2+3+4+5
    total = sum(range(1, 6))
    # Publicar el resultado y notificar a quien esté esperando
    with condicion:
        resultados[nombre] = total
        condicion.notify_all()

def main():
    condicion = threading.Condition()
    resultados = {}

    # Configuración dinámica de hilos
    nombres = ["Hilo 1", "Hilo 2"] # Se pueden agregar más hilos

    # Crear hilos en forma dinámica
    hilos = [
        threading.Thread(target=sumar, args=(nombre, condicion, resultados))
        for nombre in nombres
    ]

    # Iniciar hilos
    for t in hilos:
        t.start()

    # Esperar hasta que todos publiquen su resultado
    with condicion:
        condicion.wait_for(lambda: len(resultados) >= len(hilos))

        # Imprimir solo cuando TODOS terminaron
        print("Resultados:")
        for nombre in nombres: 
            print(f"{nombre}: {resultados[nombre]}")

    # Cierre ordenado
    for t in hilos:
        t.join()

main()
