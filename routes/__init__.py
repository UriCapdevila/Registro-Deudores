from .auth import auth_bp
from .clientes import clientes_bp
from .productos import productos_bp
from .ventas import ventas_bp
from .pagos import pagos_bp
from .dashboard import dashboard_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(dashboard_bp)