from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional

class PedidoForm(FlaskForm):
    id_cliente = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message="Seleccioná un cliente")
    ])

    fecha = DateField('Fecha del pedido', format='%Y-%m-%d', validators=[
        DataRequired(message="La fecha es obligatoria")
    ])

    estado = SelectField('Estado', choices=[
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido')
    ], validators=[
        DataRequired(message="Seleccioná un estado")
    ])

    monto_total = DecimalField('Monto total', places=2, validators=[
        DataRequired(message="El monto es obligatorio"),
        NumberRange(min=0, message="Debe ser un monto positivo")
    ])

    observaciones = TextAreaField('Observaciones', validators=[Optional()])