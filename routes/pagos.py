from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms.pagos_forms import PagoForm
from models import db, Pago, Venta

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/pagos', methods=['GET', 'POST'])
def mostrar_pagos():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus pagos')
        return redirect(url_for('auth.login'))

    form = PagoForm()
    form.venta_id.choices = [
        (v.id_venta, f"Venta #{v.id_venta} - {v.fecha.strftime('%d/%m/%Y')}")
        for v in Venta.query.filter_by(usuario_id=session['id_usuario']).order_by(Venta.fecha.desc()).all()
    ]

    if form.validate_on_submit():
        nuevo_pago = Pago(
            fecha_pago=form.fecha_pago.data,
            monto=form.monto.data,
            estado=form.estado.data,
            cuota_nro=form.cuota_nro.data,
            venta_id=form.venta_id.data,
            usuario_id=session['id_usuario']
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        flash('Pago registrado correctamente')
        return redirect(url_for('pagos.mostrar_pagos'))

    pagos = (
        db.session.query(Pago, Venta)
        .join(Venta, Pago.venta_id == Venta.id_venta)
        .filter(Pago.usuario_id == session['id_usuario'])
        .order_by(Pago.fecha_pago.desc())
        .all()
    )

    return render_template('pagos/pagos.html', pagos=pagos, form=form)

@pagos_bp.route('/pagos/eliminar/<int:id>', methods=['POST'])
def eliminar_pago(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar pagos')
        return redirect(url_for('auth.login'))

    pago = Pago.query.filter_by(id_pago=id, usuario_id=session['id_usuario']).first()

    if pago:
        db.session.delete(pago)
        db.session.commit()
        flash('Pago eliminado correctamente')
    else:
        flash('Pago no encontrado o no autorizado')

    return redirect(url_for('pagos.mostrar_pagos'))