from extensions import db

class Venta(db.Model):
    __tablename__ = 'ventas'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', backref='ventas', lazy=True)
    id_venta = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    fecha_venta = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    pagos = db.relationship('Pago', back_populates='venta')

    def __repr__(self):
        return f'<Venta {self.id_venta} - Cliente {self.cliente_id}>'