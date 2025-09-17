from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # sin contraseña
    database="registrodeudores"
)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])

    
@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('login'))  # Redirige al inicio de sesión

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)

    # Obtener ID del usuario actual
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

    # Mostrar clientes del usuario
    cursor.execute("SELECT * FROM clientes WHERE id_usuario = %s", (id_usuario,))
    lista_clientes = cursor.fetchall()

    return render_template('clientes.html', clientes=lista_clientes)

@app.route('/productos', methods=['GET', 'POST'])
def productos():
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

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
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

    # Mostrar pedidos del usuario
    cursor.execute("""
        SELECT p.*, c.nombre_cliente 
        FROM pedidos p 
        JOIN clientes c ON p.id_cliente = c.id_cliente 
        WHERE p.id_usuario = %s
    """, (id_usuario,))
    lista_pedidos = cursor.fetchall()

    return render_template('pedidos.html', pedidos=lista_pedidos, clientes=clientes)

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)

    # Obtener datos del cliente
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

if __name__ == '__main__':
    app.run(debug=True)