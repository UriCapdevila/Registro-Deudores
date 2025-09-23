from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos')
def mostrar_productos():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus productos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_usuario = %s", (session['id_usuario'],))
    productos = cursor.fetchall()
    conn.close()

    return render_template('productos/productos.html', productos=productos, current_year=2025)

@productos_bp.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para agregar productos')
        return redirect(url_for('auth.login'))

    nombre = request.form.get('nombre')
    precio_raw = request.form.get('precio')
    categoria = request.form.get('categoria') or 'Sin categoría'
    stock_raw = request.form.get('stock') or 0
    descripcion = request.form.get('descripcion') or ''

    # Validación de campos obligatorios
    if not nombre or not precio_raw:
        flash('Nombre y precio son obligatorios')
        return redirect(url_for('productos.mostrar_productos'))

    # Conversión segura
    try:
        precio = float(precio_raw)
        stock = int(stock_raw)
    except ValueError:
        flash('Precio y stock deben ser valores numéricos válidos')
        return redirect(url_for('productos.mostrar_productos'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO productos (nombre_producto, precio, categoria, stock, descripcion, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, precio, categoria, stock, descripcion, session['id_usuario']))
        conn.commit()
        flash('Producto agregado correctamente')
    except Exception as e:
        conn.rollback()
        flash(f'Error al agregar producto: {e}')
    finally:
        conn.close()

    return redirect(url_for('productos.mostrar_productos'))

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar productos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s AND id_usuario = %s", (id, session['id_usuario']))
    producto = cursor.fetchone()

    if not producto:
        flash('Producto no encontrado o no autorizado')
        conn.close()
        return redirect(url_for('productos.mostrar_productos'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        categoria = request.form.get('categoria')
        stock = request.form.get('stock')
        descripcion = request.form.get('descripcion')

        cursor.execute("""
            UPDATE productos
            SET nombre_producto = %s, precio = %s, categoria = %s, stock = %s, descripcion = %s
            WHERE id_producto = %s AND id_usuario = %s
        """, (nombre, precio, categoria, stock, descripcion, id, session['id_usuario']))
        conn.commit()
        conn.close()
        flash('Producto actualizado correctamente')
        return redirect(url_for('productos.mostrar_productos'))

    categorias = ['Bebidas', 'Alimentos', 'Electrónica', 'Higiene', 'Otros']
    conn.close()
    return render_template('productos/editar_producto.html', producto=producto, categorias=categorias, current_year=2025)

@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar productos')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s AND id_usuario = %s", (id, session['id_usuario']))
    conn.commit()
    conn.close()

    flash('Producto eliminado correctamente')
    return redirect(url_for('productos.mostrar_productos'))