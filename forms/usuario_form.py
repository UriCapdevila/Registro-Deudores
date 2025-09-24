from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    rol = SelectField('Rol', choices=[('admin', 'Admin'), ('usuario', 'Usuario')], validators=[DataRequired()])
    submit = SubmitField('Guardar')