from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos')
def mostrar_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    conn.close()
    return render_template('pedidos/pedidos.html', pedidos=pedidos)

@pedidos_bp.route('/pedidos/agregar', methods=['POST'])
def agregar_pedido():
    cliente_id = request.form['cliente_id']
    producto_id = request.form['producto_id']
    cantidad = request.form['cantidad']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (cliente_id, producto_id, cantidad) VALUES (%s, %s, %s)", (cliente_id, producto_id, cantidad))
    conn.commit()
    conn.close()
    flash('Pedido registrado correctamente')
    return redirect(url_for('pedidos.mostrar_pedidos'))