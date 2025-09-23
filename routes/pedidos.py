from flask import Blueprint, render_template, request, redirect, session, url_for
from database import get_db_connection

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    """Permite ver y agregar pedidos asociados al usuario logueado."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    id_usuario = usuario['id_usuario']

    # Obtener clientes del usuario para el formulario
    cursor.execute("SELECT id_cliente, nombre_cliente FROM clientes WHERE id_usuario = %s", (id_usuario,))
    clientes = cursor.fetchall()

    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha = request.form['fecha']
        estado = request.form['estado']
        monto_total = request.form['monto_total']
        observaciones = request.form['observaciones']

        cursor.execute("""
            INSERT INTO pedidos (id_usuario, id_cliente, fecha, estado, monto_total, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_cliente, fecha, estado, monto_total, observaciones))
        db.commit()
        return redirect(url_for('pedidos.pedidos'))

    cursor.execute("""
        SELECT p.*, c.nombre_cliente 
        FROM pedidos p 
        JOIN clientes c ON p.id_cliente = c.id_cliente 
        WHERE p.id_usuario = %s
    """, (id_usuario,))
    lista_pedidos = cursor.fetchall()
    return render_template('pedidos.html', pedidos=lista_pedidos, clientes=clientes)

@pedidos_bp.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    """Permite editar los datos de un pedido específico."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id,))
    pedido = cursor.fetchone()

    if request.method == 'POST':
        fecha = request.form['fecha']
        estado = request.form['estado']
        monto_total = request.form['monto_total']
        observaciones = request.form['observaciones']

        cursor.execute("""
            UPDATE pedidos SET 
                fecha = %s,
                estado = %s,
                monto_total = %s,
                observaciones = %s
            WHERE id_pedido = %s
        """, (fecha, estado, monto_total, observaciones, id))
        db.commit()
        return redirect(url_for('pedidos.pedidos'))

    return render_template('editar_pedido.html', pedido=pedido)

@pedidos_bp.route('/eliminar_pedido/<int:id>', methods=['POST'])
def eliminar_pedido(id):
    """Elimina un pedido específico."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id,))
    db.commit()
    return redirect(url_for('pedidos.pedidos'))
