import pika
import threading
import time
import sqlite3

def process_task(task):
    print(f"Procesando: {task}")
    time.sleep(2)
    print(f"Tarea completada: {task}")
    # Suponiendo que el resultado es simplemente un mensaje de éxito
    result = f"Completada la tarea {task}"
    store_result(task, result)


def callback(ch, method, properties, body):
    task = body.decode()
    thread = threading.Thread(target=process_task, args=(task,))
    thread.start()

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)
    print("Worker activo, esperando tareas...")
    channel.start_consuming()

def store_result(task, result):
    conn = sqlite3.connect('resultados.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS resultados (tarea TEXT, resultado TEXT)')
    cur.execute('INSERT INTO resultados (tarea, resultado) VALUES (?, ?)', (task, result))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    start_worker()
