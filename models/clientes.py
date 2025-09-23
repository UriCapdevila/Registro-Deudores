from forms.clientes_forms import ClienteForm

def insertar_cliente(cursor, cliente):
    cursor.execute(
        "INSERT INTO clientes (nombre_cliente, dni, email, telefono, direccion, observaciones) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            cliente['nombre'],
            cliente['dni'],
            cliente['email'],
            cliente['telefono'],
            cliente['direccion'],
            cliente['observaciones']
        )
    )

