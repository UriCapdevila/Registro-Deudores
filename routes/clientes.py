from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_wtf.csrf import generate_csrf
from database import get_db_connection
from forms.clientes_forms import ClienteForm

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET', 'POST'])
def mostrar_clientes():
    form = ClienteForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if form.validate_on_submit():
        cursor.execute(
            "INSERT INTO clientes (nombre_cliente, dni, email, telefono, direccion, observaciones) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                form.nombre.data,
                form.dni.data,
                form.email.data,
                form.telefono.data,
                form.direccion.data,
                form.observaciones.data
            )
        )
        conn.commit()
        flash('Cliente agregado correctamente')
        return redirect(url_for('clientes.mostrar_clientes'))

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    csrf_token = generate_csrf()
    return render_template('clientes/clientes.html', clientes=clientes, form=form, csrf_token=csrf_token)