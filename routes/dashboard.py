from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, Cliente, Producto, Venta, Pago

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para acceder al panel')
        return redirect(url_for('auth.login'))

    id_usuario = session['id_usuario']
    nombre_usuario = session.get('usuario', 'Usuario')

    # Métricas básicas
    total_clientes = Cliente.query.filter_by(usuario_id=id_usuario).count()
    total_productos = Producto.query.filter_by(usuario_id=id_usuario).count()
    total_ventas = Venta.query.filter_by(usuario_id=id_usuario).count()
    total_pagos = Pago.query.filter_by(usuario_id=id_usuario).count()

    # Ventas recientes
    ventas_recientes = Venta.query.filter_by(usuario_id=id_usuario).order_by(Venta.fecha_venta.desc()).limit(5).all()
    # Pagos recientes
    pagos_recientes = Pago.query.filter_by(usuario_id=id_usuario).order_by(Pago.fecha_pago.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        usuario=nombre_usuario,
        total_clientes=total_clientes,
        total_productos=total_productos,
        total_ventas=total_ventas,
        total_pagos=total_pagos,
        ventas_recientes=ventas_recientes,
        pagos_recientes=pagos_recientes
    )