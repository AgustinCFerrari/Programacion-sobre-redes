# Sistema de Gestión de Tareas (API Flask + SQLite)

Este proyecto implementa un servidor Flask con:
- Registro de usuarios (`POST /registro`) con contraseñas **hasheadas**.
- Login de usuarios (`POST /login`) que setea sesión por cookie firmada.
- Recurso protegido (`GET /tareas`) que devuelve un HTML de bienvenida solo si hay sesión.
- Logout (`GET /logout`).

> **Requisitos**
- Python 3.10+ (probado en 3.13)
- pip

## 1) Instalación

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install flask werkzeug

```

## 2) Comandos usados en las terminales

```bash

#Comando en terminal Servidor

python servidor.py

# Comandos en terminal del cliente

# Registro
curl -s -X POST http://127.0.0.1:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario":"nombre","contrase\u00f1a":"1234"}'

# Login y guarda cookies en cookiejar.txt
curl -s -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"nombre","contrase\u00f1a":"1234"}' \
  -c cookiejar.txt

# Acceder a /tareas (usa cookie)
curl -i http://127.0.0.1:5000/tareas -b cookiejar.txt

# Logout (lee y ESCRIBE cookiejar actualizado)
curl -i http://127.0.0.1:5000/logout -b cookiejar.txt -c cookiejar.txt

# Chequeo de logout intentando acceder a /tareas 
curl -i http://127.0.0.1:5000/tareas -b cookiejar.txt

```


