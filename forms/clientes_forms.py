from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[
        DataRequired(), Length(max=100)
    ])
    dni = StringField('DNI', validators=[
        DataRequired(), Regexp(r'^\d{7,8}$', message='DNI inválido')
    ])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=150)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Agregar cliente')