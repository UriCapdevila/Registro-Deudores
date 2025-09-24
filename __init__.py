from flask import Flask
from utils.filters import formatear_fecha, calcular_total_pagos, estado_pago

def create_app():
    app = Flask(__name__)
    app.secret_key = 'tu_clave_secreta'

    # Registrar filtros personalizados
    app.jinja_env.filters['formatear_fecha'] = formatear_fecha
    app.jinja_env.filters['calcular_total_pagos'] = calcular_total_pagos
    app.jinja_env.filters['estado_pago'] = estado_pago

    # Registrar blueprints por módulo
    from routes.auth import auth_bp
    from routes.clientes import clientes_bp
    from routes.dashboard import dashboard_bp
    from routes.pagos import pagos_bp
    from routes.productos import productos_bp
    from routes.usuarios import usuarios_bp
    from routes.ventas import ventas_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(ventas_bp)

    return app