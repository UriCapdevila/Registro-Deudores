class Venta(db.Model):
    __tablename__ = 'ventas'

    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    cliente = db.relationship('Cliente', backref='ventas', lazy=True)
    usuario = db.relationship('Usuario', backref='ventas', lazy=True)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)
    pagos = db.relationship('Pago', backref='venta', lazy=True)

    def __repr__(self):
        return f'<Venta {self.id_venta} - Cliente {self.cliente_id} - Total ${self.total}>'