class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    id_detalle = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unit = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Producto', backref='detalles', lazy=True)

    def __repr__(self):
        return f'<DetalleVenta {self.id_detalle} - Producto {self.producto_id} - Cantidad {self.cantidad}>'