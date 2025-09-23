# __init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from routes import blueprints
from database import close_db_connection

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)

    app.teardown_appcontext(close_db_connection)

    return app
