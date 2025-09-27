# views/usuarios.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Usuario
from forms.usuario_form import UsuarioForm
from utils.decorators import admin_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/gestion')
@admin_required
def gestion():
    usuarios = Usuario.query.all()
    return render_template('usuarios/gestion.html', usuarios=usuarios)

@usuarios_bp.route('/')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        nuevo = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            rol=form.rol.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/nuevo.html', form=form)

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.email = form.email.data
        usuario.rol = form.rol.data
        db.session.commit()
        flash('Usuario actualizado', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    return render_template('usuarios/editar.html', form=form)

@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))