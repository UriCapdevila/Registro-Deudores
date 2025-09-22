from .auth import auth_bp
from .dashboard import dashboard_bp
from .clientes import clientes_bp
from .productos import productos_bp
from .pedidos import pedidos_bp

# Lista de blueprints disponibles para registrar en app.py
blueprints = [
    auth_bp,
    dashboard_bp,
    clientes_bp,
    productos_bp,
    pedidos_bp
]