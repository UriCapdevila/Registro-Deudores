from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms.productos_forms import ProductoForm
from forms.auth_forms import ConfirmarLogoutForm  # ✅ CSRF para eliminar
from models import db, Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET', 'POST'])  # ✅ acepta POST
def mostrar_productos():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus productos')
        return redirect(url_for('auth.login'))

    form_agregar = ProductoForm()
    form_eliminar = ConfirmarLogoutForm()

    if form_agregar.validate_on_submit():
        try:
            # ✅ Normalizar precio: convertir coma a punto
            precio_raw = str(form_agregar.precio.data).replace(',', '.')
            precio_normalizado = float(precio_raw)

            nuevo_producto = Producto(
                nombre=form_agregar.nombre.data,
                tipo=form_agregar.tipo.data,
                precio=precio_normalizado,
                stock=form_agregar.stock.data or 0,
                descripcion=form_agregar.descripcion.data,
                usuario_id=session['id_usuario']
            )
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado correctamente')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar producto: {e}')

        return redirect(url_for('productos.mostrar_productos'))

    productos = Producto.query.filter_by(usuario_id=session['id_usuario']).all()

    return render_template(
        'productos/productos.html',
        productos=productos,
        form_agregar=form_agregar,
        form_eliminar=form_eliminar,
        current_year=2025
    )

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para editar productos')
        return redirect(url_for('auth.login'))

    producto = Producto.query.filter_by(id_producto=id, usuario_id=session['id_usuario']).first()

    if not producto:
        flash('Producto no encontrado o no autorizado')
        return redirect(url_for('productos.mostrar_productos'))

    form = ProductoForm(obj=producto)

    if form.validate_on_submit():
        try:
            precio_raw = str(form.precio.data).replace(',', '.')
            producto.precio = float(precio_raw)

            producto.nombre = form.nombre.data
            producto.tipo = form.tipo.data
            producto.stock = form.stock.data
            producto.descripcion = form.descripcion.data

            db.session.commit()
            flash('Producto actualizado correctamente')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar producto: {e}')

        return redirect(url_for('productos.mostrar_productos'))

    return render_template('productos/editar_producto.html', form=form, producto=producto, current_year=2025)

@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para eliminar productos')
        return redirect(url_for('auth.login'))

    producto = Producto.query.filter_by(id_producto=id, usuario_id=session['id_usuario']).first()

    if producto:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado correctamente')
    else:
        flash('Producto no encontrado o no autorizado')

    return redirect(url_for('productos.mostrar_productos'))