from extensions import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    direccion = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='clientes', lazy=True)
    ventas = db.relationship('Venta', back_populates='cliente', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f'<Cliente {self.nombre} - DNI {self.dni}>'