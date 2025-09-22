from flask import Flask
from config import SECRET_KEY
from routes import blueprints

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Registrar todos los blueprints desde routes/__init__.py
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
