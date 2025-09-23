from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos')
def mostrar_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos/productos.html', productos=productos)

@productos_bp.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    conn.commit()
    conn.close()
    flash('Producto agregado correctamente')
    return redirect(url_for('productos.mostrar_productos'))
