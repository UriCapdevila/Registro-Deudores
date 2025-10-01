from flask import Blueprint, render_template, redirect, session, url_for, flash
from forms.auth_forms import LoginForm, RegistroForm, ConfirmarLogoutForm
from models import db, Usuario
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.contraseña, password):
            login_user(usuario)

            session['usuario'] = usuario.nombre
            session['id_usuario'] = usuario.id_usuario
            session['rol'] = usuario.rol
            flash(f"Bienvenido, {usuario.nombre}")
            return redirect(url_for('dashboard.dashboard'))
        else:
            error = "Email o contraseña incorrectos"

    return render_template('login.html', form=form, error=error)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    error = None

    if form.validate_on_submit():
        email = form.email.data
        existente = Usuario.query.filter_by(email=email).first()

        if existente:
            error = "El email ya está registrado"
        else:
            nuevo_usuario = Usuario(
                nombre=form.nombre.data,
                email=email,
                contraseña=generate_password_hash(form.password.data),
                rol="cliente",  # ✅ Rol fijo para todos los registros
                activo=True
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            session['usuario'] = nuevo_usuario.nombre
            session['id_usuario'] = nuevo_usuario.id_usuario
            session['rol'] = nuevo_usuario.rol
            flash("Registro exitoso. Sesión iniciada.")
            return redirect(url_for('dashboard.dashboard'))

    return render_template('registro.html', form=form, error=error)

@auth_bp.route('/confirmar_logout')
def confirmar_logout():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    form = ConfirmarLogoutForm()
    return render_template('confirmar_logout.html', usuario=session['usuario'], form=form)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    usuario = session.get('usuario')
    logout_user()
    session.clear()
    print(f"Usuario '{usuario}' cerró sesión.")
    flash("Sesión cerrada correctamente.")
    return redirect(url_for('auth.login'))