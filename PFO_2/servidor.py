# servidor.py
# API Flask + SQLite con registro, login y acceso protegido a /tareas.
# - Contraseñas hasheadas con Werkzeug (nunca texto plano).
# - Persistencia en SQLite.
# - Sesión de Flask para mantener al usuario logueado.

from flask import Flask, request, jsonify, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from contextlib import closing

DB_PATH = "app.db"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-key")  # Cambiar en prod

# -----------------------------
# Helpers de base de datos
# -----------------------------
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with closing(get_db()) as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            """
        )
        con.commit()

# -----------------------------
# Endpoints
# -----------------------------

@app.post("/registro")
def registro():
    """
    Body JSON esperado: {"usuario": "nombre", "contraseña": "1234"}
    - Valida campos.
    - Hashea contraseña y guarda en SQLite.
    """

   
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario", "").strip()
    contrasenia = data.get("contraseña", "")

    if not usuario or not contrasenia:
        return jsonify({"error": "usuario y contraseña son obligatorios"}), 400

    # Hash seguro de la contraseña
    pwhash = generate_password_hash(contrasenia)

    try:
        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, pwhash),
        )
        con.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "usuario ya existe"}), 409
    finally:
        con.close()

    return jsonify({"status": "registro_ok", "usuario": usuario}), 201


@app.post("/login")
def login():
    """
    Body JSON esperado: {"usuario": "nombre", "contraseña": "1234"}
    - Verifica credenciales.
    - Si son válidas, guarda el usuario en sesión (cookie firmada).
    """
    
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario", "").strip()
    contrasenia = data.get("contraseña", "")

    if not usuario or not contrasenia:
        return jsonify({"error": "usuario y contraseña son obligatorios"}), 400

    con = get_db()
    try:
        row = con.execute(
            "SELECT id, usuario, password_hash FROM usuarios WHERE usuario = ?",
            (usuario,),
        ).fetchone()
    finally:
        con.close()

    if not row or not check_password_hash(row["password_hash"], contrasenia):
        return jsonify({"error": "credenciales inválidas"}), 401

    # Guardamos identidad mínima en sesión
    session["usuario"] = row["usuario"]
    return jsonify({"status": "login_ok", "usuario": row["usuario"]})


@app.get("/logout")
def logout():
    """ Limpia la sesión del usuario. """
    session.clear()
    return jsonify({"status": "logout_ok"})


@app.get("/tareas")
def tareas():
    """
    Recurso protegido.
    - Si hay usuario en sesión, devuelve un HTML de bienvenida.
    - Si no, devuelve 401.
    """
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"error": "no autorizado: inicie sesión"}), 401

    html = f"""
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Bienvenida</title>
        <style>
          body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 40px; }}
          .card {{
            max-width: 560px; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px;
            box-shadow: 0 1px 8px rgba(0,0,0,.06);
          }}
          h1 {{ margin-top: 0; font-size: 24px; }}
          p {{ color: #374151; }}
          code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }}
        </style>
      </head>
      <body>
        <div class="card">
          <h1>¡Hola, {usuario}! 👋</h1>
          <p>Bienvenida/o a tu sistema de tareas.</p>
          <p>Este es un HTML de bienvenida protegido por sesión.</p>
          <p>Puntos siguientes: agregar CRUD de tareas (POST/GET/PUT/DELETE).</p>
          <p><a href="/logout">Cerrar sesión</a></p>
        </div>
      </body>
    </html>
    """
    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


if __name__ == "__main__":
    # Inicializar DB al arrancar
    init_db()

    port = int(os.environ.get("PORT", "5000"))
    print(f"Servidor Flask escuchando en http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
