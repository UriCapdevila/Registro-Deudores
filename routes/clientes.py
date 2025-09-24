from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_wtf.csrf import generate_csrf
from forms.clientes_forms import ClienteForm
from models import db, Cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET', 'POST'])
def mostrar_clientes():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para acceder a tus clientes')
        return redirect(url_for('auth.login'))

    form = ClienteForm()

    if form.validate_on_submit():
        nuevo_cliente = Cliente(
            nombre=form.nombre.data,
            dni=form.dni.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            usuario_id=session['id_usuario']
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente agregado correctamente')
        return redirect(url_for('clientes.mostrar_clientes'))

    clientes = Cliente.query.filter_by(usuario_id=session['id_usuario']).all()
    csrf_token = generate_csrf()
    return render_template('clientes/clientes.html', clientes=clientes, form=form, csrf_token=csrf_token)

@clientes_bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar clientes')
        return redirect(url_for('auth.login'))

    cliente = Cliente.query.filter_by(id_cliente=id, usuario_id=session['id_usuario']).first()

    if not cliente:
        flash('Cliente no encontrado o no autorizado')
        return redirect(url_for('clientes.mostrar_clientes'))

    form = ClienteForm(obj=cliente)

    if form.validate_on_submit():
        cliente.nombre = form.nombre.data
        cliente.dni = form.dni.data
        cliente.direccion = form.direccion.data
        cliente.telefono = form.telefono.data
        db.session.commit()
        flash('Cliente actualizado correctamente')
        return redirect(url_for('clientes.mostrar_clientes'))

    return render_template('clientes/editar.html', form=form, cliente=cliente)

@clientes_bp.route('/clientes/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar clientes')
        return redirect(url_for('auth.login'))

    cliente = Cliente.query.filter_by(id_cliente=id, usuario_id=session['id_usuario']).first()

    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado correctamente')
    else:
        flash('Cliente no encontrado o no autorizado')

    return redirect(url_for('clientes.mostrar_clientes'))