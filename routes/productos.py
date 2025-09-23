from flask import Blueprint, render_template, request, redirect, session, url_for
from database import get_db_connection

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET', 'POST'])
def productos():
    """Permite ver y agregar productos asociados al usuario logueado."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    id_usuario = usuario['id_usuario']

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        stock = request.form['stock']
        descripcion = request.form['descripcion']

        cursor.execute("""
            INSERT INTO productos (id_usuario, nombre_producto, precio, categoria, stock, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, nombre, precio, categoria, stock, descripcion))
        db.commit()
        return redirect(url_for('productos.productos'))

    cursor.execute("SELECT * FROM productos WHERE id_usuario = %s", (id_usuario,))
    lista_productos = cursor.fetchall()
    return render_template('productos.html', productos=lista_productos)

@productos_bp.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    """Permite editar los datos de un producto específico."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        stock = request.form['stock']
        descripcion = request.form['descripcion']

        cursor.execute("""
            UPDATE productos SET 
                nombre_producto = %s,
                precio = %s,
                categoria = %s,
                stock = %s,
                descripcion = %s
            WHERE id_producto = %s
        """, (nombre, precio, categoria, stock, descripcion, id))
        db.commit()
        return redirect(url_for('productos.productos'))

    return render_template('editar_producto.html', producto=producto)

@productos_bp.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    """Elimina un producto específico."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    db.commit()
    return redirect(url_for('productos.productos'))
