from flask import Flask
from extensions import db, login_manager
from utils.filters import formatear_fecha, calcular_total_pagos, estado_pago
from config import Config
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # ✅ Usa configuración desde .env

    # 🔧 Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # 🔐 Configuración de Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debés iniciar sesión para acceder a esta vista'

    # 🎨 Filtros personalizados
    app.jinja_env.filters['formatear_fecha'] = formatear_fecha

    # 🧠 Funciones globales para Jinja
    app.jinja_env.globals['estado_pago'] = estado_pago
    app.jinja_env.globals['calcular_total_pagos'] = calcular_total_pagos

    # 🧪 Test de conexión
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
        except Exception as e:
            print("❌ Error de conexión:", e)

    # 📦 Blueprints
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