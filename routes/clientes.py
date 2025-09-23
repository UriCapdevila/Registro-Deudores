from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes')
def mostrar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes/clientes.html', clientes=clientes)

@clientes_bp.route('/clientes/agregar', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre, email))
    conn.commit()
    conn.close()
    flash('Cliente agregado correctamente')
    return redirect(url_for('clientes.mostrar_clientes'))
