import sqlite3
import time

# Conexión inicial solo para crear la tabla si no existe
conn = sqlite3.connect('resultados.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS resultados (tarea TEXT, resultado TEXT)')
conn.commit()
cur.close()
conn.close()

while True:
    conn = sqlite3.connect('resultados.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM resultados')
    rows = cur.fetchall()
    print("\033c")  # Limpiar pantalla 
    print("Tareas guardadas:")
    for row in rows:
        print(row)
    cur.close()
    conn.close()
    time.sleep(1)

