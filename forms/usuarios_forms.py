from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class RegistroForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=2, max=100, message="Debe tener entre 2 y 100 caracteres")
        ],
        render_kw={"class": "form-control", "placeholder": "Nombre completo"}
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Email inválido"),
            Regexp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', message="Formato de email no válido")
        ],
        render_kw={"class": "form-control", "placeholder": "ejemplo@correo.com"}
    )

    contraseña = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=6, message="Debe tener al menos 6 caracteres")
        ],
        render_kw={"class": "form-control", "placeholder": "Contraseña segura"}
    )

    rol = SelectField(
        'Rol',
        choices=[('admin', 'Administrador'), ('cliente', 'Cliente')],
        validators=[DataRequired(message="Seleccioná un rol")],
        render_kw={"class": "form-select"}
    )

    submit = SubmitField(
        'Registrar usuario',
        render_kw={"class": "btn btn-primary w-100"}
    )