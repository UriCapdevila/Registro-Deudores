from extensions import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum('carne', 'embutido', 'queso', name='tipo_producto'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    # 🔗 Relación con Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', backref='productos', lazy=True)

    def __repr__(self):
        return f'<Producto {self.nombre} - Stock {self.stock}>'