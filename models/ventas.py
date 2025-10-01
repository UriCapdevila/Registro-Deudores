from extensions import db

class Venta(db.Model):
    __tablename__ = 'ventas'

    id_venta = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente', ondelete='CASCADE'), nullable=False)
    fecha_venta = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    usuario = db.relationship('Usuario', back_populates='ventas', lazy=True)
    cliente = db.relationship('Cliente', back_populates='ventas', lazy=True)
    pagos = db.relationship('Pago', back_populates='venta', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f'<Venta {self.id_venta} - Cliente {self.cliente_id}>'