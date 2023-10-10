from flask_sqlalchemy import SQLAlchemy

# Importa otras bibliotecas que puedas necesitar, como por ejemplo:
# from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenia = db.Column(db.String(120), nullable=False)
    nombre_completo = db.Column(db.String(120), nullable=False)
    roles = db.Column(db.String(120), nullable=False)
