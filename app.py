# ---------------------------
# IMPORTACIONES Y CONFIGURACIÓN
# ---------------------------
from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import hashlib
import os

# ---------------------------
# INICIALIZACIÓN DE LA APP
# ---------------------------
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Clave para manejar sesiones de usuario

# ---------------------------
# CONEXIÓN A LA BASE DE DATOS
# ---------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # sin contraseña
    database="registrodeudores"
)

# ---------------------------
# RUTAS PRINCIPALES Y AUTENTICACIÓN
# ---------------------------

@app.route('/')
def home():
    """Redirige a la página de login."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Muestra el formulario de login y valida credenciales.
    Si el usuario y contraseña son correctos, inicia sesión.
    """
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM usuarios 
            WHERE nombre_usuario = %s AND contrasena_hash = %s
        """, (username, hashed_pw))
        user = cursor.fetchone()

        if user:
            session['usuario'] = user['nombre_usuario']
            return redirect(url_for('dashboard'))
        else:
            error = "Usuario o contraseña incorrectos"
    
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    """
    Muestra el panel principal si el usuario está autenticado.
    """
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """
    Cierra la sesión del usuario y lo redirige al login.
    """
    session.clear()
    return redirect(url_for('login'))

# ---------------------------
# GESTIÓN DE CLIENTES
# ---------------------------

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    """
    Permite ver y agregar clientes asociados al usuario logueado.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    id_usuario = usuario['id_usuario']

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        observaciones = request.form['observaciones']

        cursor.execute("""
            INSERT INTO clientes (id_usuario, nombre_cliente, dni, email, telefono, direccion, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, nombre, dni, email, telefono, direccion, observaciones))
        db.commit()
        return redirect(url_for('clientes'))

    cursor.execute("SELECT * FROM clientes WHERE id_usuario = %s", (id_usuario,))
    lista_clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=lista_clientes)

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    """
    Permite editar los datos de un cliente específico.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        observaciones = request.form['observaciones']

        cursor.execute("""
            UPDATE clientes SET 
                nombre_cliente = %s,
                dni = %s,
                email = %s,
                telefono = %s,
                direccion = %s,
                observaciones = %s
            WHERE id_cliente = %s
        """, (nombre, dni, email, telefono, direccion, observaciones, id))
        db.commit()
        return redirect(url_for('clientes'))

    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    """
    Elimina un cliente específico.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
    db.commit()
    return redirect(url_for('clientes'))

# ---------------------------
# GESTIÓN DE PRODUCTOS
# ---------------------------

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    """
    Permite ver y agregar productos asociados al usuario logueado.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    id_usuario = usuario['id_usuario']

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        stock = request.form['stock']
        descripcion = request.form['descripcion']

        cursor.execute("""
            INSERT INTO productos (id_usuario, nombre_producto, precio, categoria, stock, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, nombre, precio, categoria, stock, descripcion))
        db.commit()
        return redirect(url_for('productos'))

    cursor.execute("SELECT * FROM productos WHERE id_usuario = %s", (id_usuario,))
    lista_productos = cursor.fetchall()
    return render_template('productos.html', productos=lista_productos)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    """
    Permite editar los datos de un producto específico.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        stock = request.form['stock']
        descripcion = request.form['descripcion']

        cursor.execute("""
            UPDATE productos SET 
                nombre_producto = %s,
                precio = %s,
                categoria = %s,
                stock = %s,
                descripcion = %s
            WHERE id_producto = %s
        """, (nombre, precio, categoria, stock, descripcion, id))
        db.commit()
        return redirect(url_for('productos'))

    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    """
    Elimina un producto específico.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    db.commit()
    return redirect(url_for('productos'))

# ---------------------------
# GESTIÓN DE PEDIDOS
# ---------------------------

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    """
    Permite ver y agregar pedidos asociados al usuario logueado.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    id_usuario = usuario['id_usuario']

    # Obtener clientes del usuario para el formulario
    cursor.execute("SELECT id_cliente, nombre_cliente FROM clientes WHERE id_usuario = %s", (id_usuario,))
    clientes = cursor.fetchall()

    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha = request.form['fecha']
        estado = request.form['estado']
        monto_total = request.form['monto_total']
        observaciones = request.form['observaciones']

        cursor.execute("""
            INSERT INTO pedidos (id_usuario, id_cliente, fecha, estado, monto_total, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_cliente, fecha, estado, monto_total, observaciones))
        db.commit()
        return redirect(url_for('pedidos'))

    cursor.execute("""
        SELECT p.*, c.nombre_cliente 
        FROM pedidos p 
        JOIN clientes c ON p.id_cliente = c.id_cliente 
        WHERE p.id_usuario = %s
    """, (id_usuario,))
    lista_pedidos = cursor.fetchall()
    return render_template('pedidos.html', pedidos=lista_pedidos, clientes=clientes)

@app.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    """
    Permite editar los datos de un pedido específico.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id,))
    pedido = cursor.fetchone()

    if request.method == 'POST':
        fecha = request.form['fecha']
        estado = request.form['estado']
        monto_total = request.form['monto_total']
        observaciones = request.form['observaciones']

        cursor.execute("""
            UPDATE pedidos SET 
                fecha = %s,
                estado = %s,
                monto_total = %s,
                observaciones = %s
            WHERE id_pedido = %s
        """, (fecha, estado, monto_total, observaciones, id))
        db.commit()
        return redirect(url_for('pedidos'))

    return render_template('editar_pedido.html', pedido=pedido)

@app.route('/eliminar_pedido/<int:id>', methods=['POST'])
def eliminar_pedido(id):
    """
    Elimina un pedido específico.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id,))
    db.commit()
    return redirect(url_for('pedidos'))

# ---------------------------
# INICIO DE LA APLICACIÓN
# ---------------------------
if __name__ == '__main__':
    # Permite activar el modo debug desde la variable de entorno FLASK_DEBUG
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)