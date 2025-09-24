from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos los modelos
from .clientes import Cliente
from .pagos import Pago
from .ventas import Venta
from .detalleventa import DetalleVenta
from .productos import Producto
from .usuarios import Usuario
