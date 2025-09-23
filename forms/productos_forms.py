from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[DataRequired(message="El nombre es obligatorio")])

    precio = DecimalField('Precio', places=2, rounding=None,
                          validators=[DataRequired(message="El precio es obligatorio"),
                                      NumberRange(min=0, message="El precio debe ser positivo")])

    categoria = SelectField('Categoría', choices=[
        ('Bebidas', 'Bebidas'),
        ('Alimentos', 'Alimentos'),
        ('Electrónica', 'Electrónica'),
        ('Higiene', 'Higiene'),
        ('Otros', 'Otros')
    ], validators=[Optional()])

    stock = IntegerField('Stock disponible', validators=[
        Optional(),
        NumberRange(min=0, message="El stock no puede ser negativo")
    ])

    descripcion = TextAreaField('Descripción', validators=[Optional()])

    