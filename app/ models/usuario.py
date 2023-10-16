import datetime
from flask_sqlalchemy import SQLAlchemy

# Importa otras bibliotecas que puedas necesitar, como por ejemplo:
# from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __table_name = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    date_registered = db.Column(db.DateTime, default = datetime.utcnow())
    