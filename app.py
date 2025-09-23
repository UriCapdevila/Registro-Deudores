# app.py
from __init__ import create_app
import os

app = create_app()

# 🔍 Verificador de endpoints registrados
print("\n📋 Endpoints registrados en Flask:")
for rule in app.url_map.iter_rules():
    methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
    print(f"🔹 {rule.endpoint:30} → {rule.rule:40} [Métodos: {methods}]")
print("✅ Verificación completa\n")

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
