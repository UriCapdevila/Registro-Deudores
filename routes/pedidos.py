from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['GET', 'POST'])
def mostrar_pedidos():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus pedidos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # ✅ Evita errores de tipo tupla

    # Registrar nuevo pedido si se envió el formulario
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        fecha = request.form.get('fecha')
        estado = request.form.get('estado')
        monto_total = request.form.get('monto_total')
        observaciones = request.form.get('observaciones')

        # Validación básica
        if not id_cliente or not fecha or not estado or not monto_total:
            flash('Todos los campos obligatorios deben estar completos')
            return redirect(url_for('pedidos.mostrar_pedidos'))

        try:
            cursor.execute("""
                INSERT INTO pedidos (id_cliente, fecha, estado, monto_total, observaciones, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_cliente, fecha, estado, monto_total, observaciones, session['id_usuario']))
            conn.commit()
            flash('Pedido registrado correctamente')
        except Exception as e:
            conn.rollback()
            flash(f'Error al registrar el pedido: {e}')
        return redirect(url_for('pedidos.mostrar_pedidos'))

    # Obtener clientes del usuario activo
    cursor.execute("""
        SELECT id_cliente, nombre_cliente
        FROM clientes
        WHERE id_usuario = %s
        ORDER BY nombre_cliente ASC
    """, (session['id_usuario'],))
    clientes = cursor.fetchall()

    # Obtener pedidos del usuario activo con nombre del cliente
    cursor.execute("""
        SELECT pedidos.id_pedido, pedidos.fecha, pedidos.estado, pedidos.monto_total, pedidos.observaciones,
               clientes.nombre_cliente
        FROM pedidos
        JOIN clientes ON pedidos.id_cliente = clientes.id_cliente
        WHERE pedidos.id_usuario = %s
        ORDER BY pedidos.fecha DESC
    """, (session['id_usuario'],))
    pedidos = cursor.fetchall()

    conn.close()
    return render_template('pedidos/pedidos.html', pedidos=pedidos, clientes=clientes)

@pedidos_bp.route('/pedidos/editar/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar pedidos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener el pedido
    cursor.execute("""
        SELECT * FROM pedidos
        WHERE id_pedido = %s AND id_usuario = %s
    """, (id, session['id_usuario']))
    pedido = cursor.fetchone()

    if not pedido:
        flash('Pedido no encontrado o no autorizado')
        conn.close()
        return redirect(url_for('pedidos.mostrar_pedidos'))

    if request.method == 'POST':
        estado = request.form.get('estado')
        monto_total = request.form.get('monto_total')
        observaciones = request.form.get('observaciones')

        try:
            cursor.execute("""
                UPDATE pedidos
                SET estado = %s, monto_total = %s, observaciones = %s
                WHERE id_pedido = %s AND id_usuario = %s
            """, (estado, monto_total, observaciones, id, session['id_usuario']))
            conn.commit()
            flash('Pedido actualizado correctamente')
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar el pedido: {e}')
        finally:
            conn.close()

        return redirect(url_for('pedidos.mostrar_pedidos'))

    conn.close()
    return render_template('pedidos/editar_pedido.html', pedido=pedido, current_year=2025)