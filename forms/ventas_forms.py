from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, DecimalField, SubmitField
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