from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('admin', 'cliente', name='rol_usuario'), nullable=False, default='cliente')
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Usuario {self.email} - Rol {self.rol}>'