from flask import Blueprint, render_template, request, redirect, session, url_for
from config import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET', 'POST'])
def clientes():
    """Permite ver y agregar clientes asociados al usuario logueado."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    id_usuario = usuario['id_usuario']

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        observaciones = request.form['observaciones']

        cursor.execute("""
            INSERT INTO clientes (id_usuario, nombre_cliente, dni, email, telefono, direccion, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, nombre, dni, email, telefono, direccion, observaciones))
        db.commit()
        return redirect(url_for('clientes.clientes'))

    cursor.execute("SELECT * FROM clientes WHERE id_usuario = %s", (id_usuario,))
    lista_clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=lista_clientes)

@clientes_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    """Permite editar los datos de un cliente específico."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        observaciones = request.form['observaciones']

        cursor.execute("""
            UPDATE clientes SET 
                nombre_cliente = %s,
                dni = %s,
                email = %s,
                telefono = %s,
                direccion = %s,
                observaciones = %s
            WHERE id_cliente = %s
        """, (nombre, dni, email, telefono, direccion, observaciones, id))
        db.commit()
        return redirect(url_for('clientes.clientes'))

    return render_template('editar_cliente.html', cliente=cliente)

@clientes_bp.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    """Elimina un cliente específico."""
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
    db.commit()
    return redirect(url_for('clientes.clientes'))

    print(f"Usuario {usuario} ha cerrado sesión.")  

    