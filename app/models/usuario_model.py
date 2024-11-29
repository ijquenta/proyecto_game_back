from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'game'}  # Especifica el esquema

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # ID generado automáticamente
    username = db.Column(db.Text, nullable=False, unique=True)  # Nombre de usuario único
    email = db.Column(db.Text, nullable=False, unique=True)  # Correo electrónico único

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }