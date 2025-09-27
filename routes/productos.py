from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms.productos_forms import ProductoForm
from models import db, Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos')
def mostrar_productos():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para ver tus productos')
        return redirect(url_for('auth.login'))

    productos = Producto.query.filter_by(usuario_id=session['id_usuario']).all()
    form = ProductoForm()  # ✅ Se agregó el formulario

    return render_template('productos/productos.html', productos=productos, form=form, current_year=2025)

@productos_bp.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if 'id_usuario' not in session:
        flash('Debés iniciar sesión para agregar productos')
        return redirect(url_for('auth.login'))

    form = ProductoForm()

    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            tipo=form.tipo.data,
            precio=form.precio.data,
            stock=form.stock.data or 0,
            descripcion=form.descripcion.data,
            usuario_id=session['id_usuario']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto agregado correctamente')
        return redirect(url_for('productos.mostrar_productos'))

    return render_template('productos/agregar_producto.html', form=form, current_year=2025)

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
        producto.nombre = form.nombre.data
        producto.tipo = form.tipo.data
        producto.precio = form.precio.data
        producto.stock = form.stock.data
        producto.descripcion = form.descripcion.data
        db.session.commit()
        flash('Producto actualizado correctamente')
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