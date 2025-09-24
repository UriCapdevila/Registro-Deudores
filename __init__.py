from flask import Flask
from utils.filters import formatear_fecha, calcular_total_pagos, estado_pago

def create_app():
    app = Flask(__name__)
    app.secret_key = 'tu_clave_secreta'

    # Registrar filtros
    app.jinja_env.filters['formatear_fecha'] = formatear_fecha
    app.jinja_env.filters['calcular_total_pagos'] = calcular_total_pagos
    app.jinja_env.filters['estado_pago'] = estado_pago

    # Registrar blueprints, extensiones, etc.
    # from views.clientes import clientes_bp
    # app.register_blueprint(clientes_bp)

    return app