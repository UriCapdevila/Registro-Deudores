from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class VentaForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message="Seleccioná un cliente")
    ])
    fecha = DateField('Fecha de la venta', format='%Y-%m-%d', validators=[
        DataRequired(message="La fecha es obligatoria")
    ])
    total = DecimalField('Monto total', places=2, validators=[
        DataRequired(message="El monto es obligatorio"),
        NumberRange(min=0, message="Debe ser un monto positivo")
    ])
    submit = SubmitField('Registrar venta')

class DetalleVentaForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, validators=[
        DataRequired(message="Seleccioná un producto")
    ])
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria"),
        NumberRange(min=1, message="Debe ser al menos 1 unidad")
    ])
    precio_unitario = DecimalField('Precio unitario', places=2, validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0, message="Debe ser un precio positivo")
    ])
    submit = SubmitField('Agregar al detalle')