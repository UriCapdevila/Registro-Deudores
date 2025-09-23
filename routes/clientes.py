from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_wtf.csrf import generate_csrf
from database import get_db_connection
from forms.clientes_forms import ClienteForm

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET', 'POST'])
def mostrar_clientes():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para acceder a tus clientes')
        return redirect(url_for('auth.login'))

    form = ClienteForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if form.validate_on_submit():
        cursor.execute(
            "INSERT INTO clientes (nombre_cliente, dni, email, telefono, direccion, observaciones, id_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                form.nombre.data,
                form.dni.data,
                form.email.data,
                form.telefono.data,
                form.direccion.data,
                form.observaciones.data,
                session['id_usuario']  # ✅ clave para vincular cliente al usuario
            )
        )
        conn.commit()
        flash('Cliente agregado correctamente')
        return redirect(url_for('clientes.mostrar_clientes'))

    # ✅ Mostrar solo los clientes del usuario activo
    cursor.execute("SELECT * FROM clientes WHERE id_usuario = %s", (session['id_usuario'],))
    clientes = cursor.fetchall()
    conn.close()

    csrf_token = generate_csrf()
    return render_template('clientes/clientes.html', clientes=clientes, form=form, csrf_token=csrf_token)

@clientes_bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar clientes')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Asegurarse de que el cliente pertenece al usuario activo
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s AND id_usuario = %s", (id, session['id_usuario']))
    cliente = cursor.fetchone()

    if not cliente:
        flash('Cliente no encontrado o no autorizado')
        conn.close()
        return redirect(url_for('clientes.mostrar_clientes'))

    form = ClienteForm(data={
        'nombre': cliente['nombre_cliente'],
        'dni': cliente['dni'],
        'email': cliente['email'],
        'telefono': cliente['telefono'],
        'direccion': cliente['direccion'],
        'observaciones': cliente['observaciones']
    })

    if form.validate_on_submit():
        cursor.execute("""
            UPDATE clientes SET nombre_cliente=%s, dni=%s, email=%s, telefono=%s, direccion=%s, observaciones=%s
            WHERE id_cliente=%s AND id_usuario=%s
        """, (
            form.nombre.data,
            form.dni.data,
            form.email.data,
            form.telefono.data,
            form.direccion.data,
            form.observaciones.data,
            id,
            session['id_usuario']
        ))
        conn.commit()
        flash('Cliente actualizado correctamente')
        return redirect(url_for('clientes.mostrar_clientes'))

    conn.close()
    return render_template('clientes/editar.html', form=form, cliente=cliente)

@clientes_bp.route('/clientes/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar clientes')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Asegurarse de que el cliente pertenece al usuario activo
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s AND id_usuario = %s", (id, session['id_usuario']))
    conn.commit()
    conn.close()

    flash('Cliente eliminado correctamente')
    return redirect(url_for('clientes.mostrar_clientes'))