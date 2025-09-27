from extensions import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum('carne', 'embutido', 'queso', name='tipo_producto'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(300), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('productos', lazy=True))

    def __repr__(self):
        return f'<Producto {self.nombre} - Stock {self.stock} - Activo {self.activo}>'