from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2.extras import RealDictCursor 

app = Flask(__name__)

# Render inyecta la URL de la base de datos externa aquí
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    # Conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM videojuegos")
    videojuegos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", videojuegos=videojuegos)

@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        plataforma = request.form["plataforma"]

        conn = get_db_connection()
        cur = conn.cursor()
        # PostgreSQL usa %s como marcador de posición
        cur.execute(
            "INSERT INTO videojuegos (nombre, precio, plataforma) VALUES (%s, %s, %s)",
            (nombre, precio, plataforma),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM videojuegos WHERE id = %s", (id,))
    videojuego = cur.fetchone()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        plataforma = request.form["plataforma"]

        cur.execute(
            "UPDATE videojuegos SET nombre=%s, precio=%s, plataforma=%s WHERE id=%s",
            (nombre, precio, plataforma, id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    cur.close()
    conn.close()
    return render_template("edit.html", videojuego=videojuego)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM videojuegos WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
