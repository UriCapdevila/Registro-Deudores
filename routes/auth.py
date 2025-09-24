from flask import Blueprint, render_template, redirect, session, url_for, flash
from forms.auth_forms import LoginForm, RegistroForm
from models import db, Usuario
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
            session['usuario'] = usuario.nombre
            session['id_usuario'] = usuario.id_usuario
            session['rol'] = usuario.rol  # ✅ Guardamos el rol
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
                rol=form.rol.data,  # ✅ Rol desde el formulario
                activo=True
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            session['usuario'] = nuevo_usuario.nombre
            session['id_usuario'] = nuevo_usuario.id_usuario
            session['rol'] = nuevo_usuario.rol  # ✅ Guardamos el rol
            flash("Registro exitoso. Sesión iniciada.")
            return redirect(url_for('dashboard.dashboard'))

    return render_template('registro.html', form=form, error=error)

@auth_bp.route('/confirmar_logout')
def confirmar_logout():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    return render_template('confirmar_logout.html', usuario=session['usuario'])

@auth_bp.route('/logout', methods=['POST'])
def logout():
    usuario = session.get('usuario')
    session.pop('usuario', None)
    session.pop('id_usuario', None)
    session.pop('rol', None)  # ✅ Limpiamos el rol también
    print(f"Usuario '{usuario}' cerró sesión.")
    flash("Sesión cerrada correctamente.")
    return redirect(url_for('auth.login'))