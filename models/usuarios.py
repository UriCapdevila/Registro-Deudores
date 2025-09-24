from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models.usuarios import Usuario
from forms.usuarios_forms import RegistroForm
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        # Limpieza de datos
        nombre = form.nombre.data.strip()
        email = form.email.data.strip().lower()
        contraseña = generate_password_hash(form.contraseña.data)
        rol = form.rol.data

        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
            return render_template('usuarios/registro.html', form=form)

        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            contraseña=contraseña,
            rol=rol,
            activo=True
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('auth.login'))  # o dashboard, según tu flujo
        except IntegrityError:
            db.session.rollback()
            flash('Error al registrar el usuario. Intentalo nuevamente.', 'danger')

    return render_template('usuarios/registro.html', form=form)