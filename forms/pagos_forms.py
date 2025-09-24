from extensions import db
from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class PagoForm(FlaskForm):
    fecha_pago = DateField('Fecha de pago', validators=[DataRequired()], format='%Y-%m-%d')
    monto = DecimalField('Monto', validators=[DataRequired(), NumberRange(min=0)], places=2)
    estado = SelectField('Estado del pago', choices=[
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
        ('completo', 'Completo')
    ], validators=[DataRequired()])
    cuota_nro = IntegerField('Número de cuota', validators=[Optional()])
    submit = SubmitField('Registrar pago')