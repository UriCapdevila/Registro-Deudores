from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, Optional, Email

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[
        DataRequired(), Length(max=100)
    ])
    dni = StringField('DNI', validators=[
        DataRequired(), Regexp(r'^\d{7,8}$', message='DNI inválido')
    ])
    email = StringField('Email', validators=[
        Optional(), Email(message='Email inválido'), Length(max=100)
    ])
    direccion = StringField('Dirección', validators=[
        Optional(), Length(max=150)
    ])
    telefono = StringField('Teléfono', validators=[
        Optional(), Length(max=20)
    ])
    observaciones = TextAreaField('Observaciones', validators=[
        Optional(), Length(max=500)
    ])
    submit = SubmitField('Agregar cliente')