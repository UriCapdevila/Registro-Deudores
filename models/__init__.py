from flask_sqlalchemy import SQLAlchemy
from extensions import db  # ✅ Usa la instancia ya vinculada

# Importar todos los modelos
from .usuarios import Usuario
from .clientes import Cliente
from .pagos import Pago
from .ventas import Venta
from .detalleventa import DetalleVenta
from .productos import Producto

