from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired()])
    dni = StringField('DNI', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    telefono = StringField('Teléfono', validators=[Optional()])
    direccion = StringField('Dirección', validators=[Optional()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Agregar cliente')