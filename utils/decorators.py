from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

# Solo permite acceso a administradores
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('Acceso restringido: solo administradores', 'danger')
            return redirect(url_for('dashboard.dashboard'))  # ✅ corregido
        return f(*args, **kwargs)
    return decorated_function

# Permite acceso solo a usuarios con rol específico
def rol_required(rol):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol != rol:
                flash(f'Acceso restringido a usuarios con rol: {rol}', 'danger')
                return redirect(url_for('dashboard.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper