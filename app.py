# app.py
from __init__ import create_app
import os

app = create_app()


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)

from utils.filters import formatear_fecha, calcular_total_pagos, estado_pago

def create_app():
    app = Flask(__name__)
    ...
    app.jinja_env.filters['formatear_fecha'] = formatear_fecha
    app.jinja_env.filters['calcular_total_pagos'] = calcular_total_pagos
    app.jinja_env.filters['estado_pago'] = estado_pago
    ...
    return app