from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from forms.ventas_forms import VentaForm
from models import db, Venta, Cliente

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas', methods=['GET', 'POST'])
def mostrar_ventas():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus ventas')
        return redirect(url_for('auth.login'))

    form = VentaForm()
    form.cliente_id.choices = [
        (c.id_cliente, c.nombre)
        for c in Cliente.query.filter_by(usuario_id=session['id_usuario']).order_by(Cliente.nombre.asc()).all()
    ]

    if form.validate_on_submit():
        nueva_venta = Venta(
            cliente_id=form.cliente_id.data,
            fecha_venta=form.fecha.data,  # ✅ campo correcto
            total=form.total.data,
            usuario_id=session['id_usuario']
        )
        db.session.add(nueva_venta)
        db.session.commit()
        flash('Venta registrada correctamente')
        return redirect(url_for('ventas.mostrar_ventas'))

    ventas = (
        db.session.query(Venta, Cliente)
        .join(Cliente, Venta.cliente_id == Cliente.id_cliente)
        .filter(Venta.usuario_id == session['id_usuario'])
        .order_by(Venta.fecha_venta.desc())  # ✅ campo correcto
        .all()
    )

    return render_template('ventas/ventas.html', ventas=ventas, form=form)

@ventas_bp.route('/ventas/editar/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar ventas')
        return redirect(url_for('auth.login'))

    venta = Venta.query.filter_by(id_venta=id, usuario_id=session['id_usuario']).first()

    if not venta:
        flash('Venta no encontrada o no autorizada')
        return redirect(url_for('ventas.mostrar_ventas'))

    form = VentaForm(obj=venta)
    form.cliente_id.choices = [
        (c.id_cliente, c.nombre)
        for c in Cliente.query.filter_by(usuario_id=session['id_usuario']).order_by(Cliente.nombre.asc()).all()
    ]

    if form.validate_on_submit():
        venta.cliente_id = form.cliente_id.data
        venta.fecha_venta = form.fecha.data  # ✅ campo correcto
        venta.total = form.total.data
        db.session.commit()
        flash('Venta actualizada correctamente')
        return redirect(url_for('ventas.mostrar_ventas'))

    return render_template('ventas/editar_venta.html', form=form, venta=venta)

@ventas_bp.route('/ventas/eliminar/<int:id>', methods=['POST'])
def eliminar_venta(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar ventas')
        return redirect(url_for('auth.login'))

    venta = Venta.query.filter_by(id_venta=id, usuario_id=session['id_usuario']).first()

    if venta:
        db.session.delete(venta)
        db.session.commit()
        flash('Venta eliminada correctamente')
    else:
        flash('Venta no encontrada o no autorizada')

    return redirect(url_for('ventas.mostrar_ventas'))