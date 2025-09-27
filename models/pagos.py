from extensions import db

class Pago(db.Model):
    __tablename__ = 'pagos'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', backref='pagos', lazy=True)
    id_pago = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'parcial', 'completo', name='estado_pago'), nullable=False, default='pendiente')
    cuota_nro = db.Column(db.Integer)

    venta = db.relationship('Venta', back_populates='pagos')

    def __repr__(self):
        return f'<Pago {self.id_pago} - Venta {self.venta_id} - Estado {self.estado}>'