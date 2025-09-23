from flask import Blueprint, render_template, redirect, session, url_for, flash
from database import get_db_connection
from forms.auth_forms import LoginForm, RegistroForm
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user['contrasena_hash'].encode()):
            session['usuario'] = user['nombre_usuario']
            return redirect(url_for('dashboard.dashboard'))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template('login.html', form=form, error=error)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (username,))
        existente = cursor.fetchone()

        if existente:
            error = "El nombre de usuario ya está en uso"
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena_hash) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            conn.close()
            return redirect(url_for('auth.login'))

        conn.close()

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
    print(f"Usuario '{usuario}' cerró sesión.")
    return redirect(url_for('auth.login'))