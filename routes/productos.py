from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from forms.productos_forms import ProductoForm

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

@productos_bp.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para agregar productos')
        return redirect(url_for('auth.login'))

    form = ProductoForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre_producto, precio, categoria, stock, descripcion, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            float(form.precio.data),
            form.categoria.data,
            form.stock.data or 0,
            form.descripcion.data or '',
            session['id_usuario']
        ))
        conn.commit()
        conn.close()
        flash('Producto agregado correctamente')
        return redirect(url_for('productos.mostrar_productos'))

    return render_template('productos/agregar_producto.html', form=form, current_year=2025)

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