from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# class Persona2(db.Model):
#     __tablename__ = 'persona'
#     __table_args__ = {'schema': 'academico'}
#     perid = db.Column(db.Integer, primary_key=True)
#     pernomcompleto = db.Column(db.String)
#     pernombres = db.Column(db.String(100), nullable=False)
#     perapepat = db.Column(db.String(100))
#     perapemat = db.Column(db.String(100))
#     pertipodoc = db.Column(db.Integer)
#     pernrodoc = db.Column(db.Integer)
#     perfecnac = db.Column(db.Date)
#     perdirec = db.Column(db.Text)
#     peremail = db.Column(db.String(100))
#     percelular = db.Column(db.String(20))
#     pertelefono = db.Column(db.String(20))
#     perpais = db.Column(db.Integer)
#     perciudad = db.Column(db.Integer)
#     pergenero = db.Column(db.Integer)
#     perestcivil = db.Column(db.Integer)
#     perfoto = db.Column(db.String)
#     perestado = db.Column(db.SmallInteger, default=1)
#     perobservacion = db.Column(db.String(255))
#     perusureg = db.Column(db.String(50))
#     perfecreg = db.Column(db.TIMESTAMP, default=db.func.now())
#     perusumod = db.Column(db.String(50))
#     perfecmod = db.Column(db.TIMESTAMP)