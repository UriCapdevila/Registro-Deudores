from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(max=100)
    ])

    tipo = SelectField('Tipo de producto', choices=[
        ('carne', 'Carne'),
        ('embutido', 'Embutido'),
        ('queso', 'Queso')
    ], validators=[DataRequired(message="Seleccioná un tipo")])

    precio = DecimalField('Precio', places=2, validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0, message="El precio debe ser positivo")
    ])

    stock = IntegerField('Stock disponible', validators=[
        DataRequired(message="El stock es obligatorio"),
        NumberRange(min=0, message="El stock no puede ser negativo")
    ])

    submit = SubmitField('Guardar producto')