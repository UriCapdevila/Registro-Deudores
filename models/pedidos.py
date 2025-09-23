from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos')
def mostrar_pedidos():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus pedidos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, c.nombre_cliente
        FROM pedidos p
        LEFT JOIN clientes c ON p.id_cliente = c.id_cliente
        WHERE p.id_usuario = %s
        ORDER BY p.fecha DESC
    """, (session['id_usuario'],))
    pedidos = cursor.fetchall()

    cursor.execute("SELECT id_cliente, nombre_cliente FROM clientes WHERE id_usuario = %s", (session['id_usuario'],))
    clientes = cursor.fetchall()

    conn.close()
    return render_template('pedidos/pedidos.html', pedidos=pedidos, clientes=clientes, current_year=2025)

@pedidos_bp.route('/pedidos/registrar', methods=['POST'])
def registrar_pedido():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para registrar pedidos')
        return redirect(url_for('auth.login'))

    id_cliente = request.form.get('id_cliente')
    fecha = request.form.get('fecha')
    estado = request.form.get('estado') or 'pendiente'
    monto_raw = request.form.get('monto_total')
    observaciones = request.form.get('observaciones') or ''

    # Validación básica
    if not id_cliente or not fecha or not monto_raw:
        flash('Todos los campos obligatorios deben estar completos')
        return redirect(url_for('pedidos.mostrar_pedidos'))

    try:
        monto_total = float(monto_raw.replace(',', '.'))
    except ValueError:
        flash('El monto debe ser un número válido')
        return redirect(url_for('pedidos.mostrar_pedidos'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO pedidos (id_cliente, fecha, estado, monto_total, observaciones, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_cliente, fecha, estado, monto_total, observaciones, session['id_usuario']))
        conn.commit()
        flash('Pedido registrado correctamente')
    except Exception as e:
        conn.rollback()
        flash(f'Error al registrar pedido: {e}')
    finally:
        conn.close()

    return redirect(url_for('pedidos.mostrar_pedidos'))

@pedidos_bp.route('/pedidos/editar/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar pedidos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, c.nombre_cliente
        FROM pedidos p
        LEFT JOIN clientes c ON p.id_cliente = c.id_cliente
        WHERE p.id_pedido = %s AND p.id_usuario = %s
    """, (id, session['id_usuario']))
    pedido = cursor.fetchone()

    if not pedido:
        flash('Pedido no encontrado o no autorizado')
        conn.close()
        return redirect(url_for('pedidos.mostrar_pedidos'))

    if request.method == 'POST':
        estado = request.form.get('estado') or 'pendiente'
        monto_raw = request.form.get('monto_total')
        observaciones = request.form.get('observaciones') or ''

        try:
            monto_total = float(monto_raw.replace(',', '.'))
        except ValueError:
            flash('El monto debe ser un número válido')
            return redirect(url_for('pedidos.editar_pedido', id=id))

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
            flash(f'Error al actualizar pedido: {e}')
        finally:
            conn.close()

        return redirect(url_for('pedidos.mostrar_pedidos'))

    conn.close()
    return render_template('pedidos/editar_pedido.html', pedido=pedido, current_year=2025)

@pedidos_bp.route('/pedidos/eliminar/<int:id>', methods=['POST'])
def eliminar_pedido(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar pedidos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM pedidos
            WHERE id_pedido = %s AND id_usuario = %s
        """, (id, session['id_usuario']))
        conn.commit()
        flash('Pedido eliminado correctamente')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar pedido: {e}')
    finally:
        conn.close()

    return redirect(url_for('pedidos.mostrar_pedidos'))