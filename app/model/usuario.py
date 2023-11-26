from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# from model.persona import Persona2
class Persona(db.Model):
    __tablename__ = 'persona'
    __table_args__ = {'schema': 'academico'}
    perid = db.Column(db.Integer, primary_key=True)
    pernomcompleto = db.Column(db.String)
    pernombres = db.Column(db.String(100), nullable=False)
    perapepat = db.Column(db.String(100))
    perapemat = db.Column(db.String(100))
    pertipodoc = db.Column(db.Integer)
    pernrodoc = db.Column(db.Integer)
    perfecnac = db.Column(db.Date)
    perdirec = db.Column(db.Text)
    peremail = db.Column(db.String(100))
    percelular = db.Column(db.String(20))
    pertelefono = db.Column(db.String(20))
    perpais = db.Column(db.Integer)
    perciudad = db.Column(db.Integer)
    pergenero = db.Column(db.Integer)
    perestcivil = db.Column(db.Integer)
    perfoto = db.Column(db.String)
    perestado = db.Column(db.SmallInteger, default=1)
    perobservacion = db.Column(db.String(255))
    perusureg = db.Column(db.String(50))
    perfecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    perusumod = db.Column(db.String(50))
    perfecmod = db.Column(db.TIMESTAMP)

class Rol(db.Model):
    __tablename__ = 'rol'
    __table_args__ = {'schema': 'academico'}
    rolid = db.Column(db.Integer, primary_key=True)
    rolnombre = db.Column(db.String(50), nullable=False)
    roldescripcion = db.Column(db.String(255))
    rolusureg = db.Column(db.String(50))
    rolfecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    rolusumod = db.Column(db.String(50))
    rolfecmod = db.Column(db.TIMESTAMP)
    rolestado = db.Column(db.SmallInteger, default=1)
    
class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'academico'}
    usuid = db.Column(db.Integer, primary_key=True)
    perid = db.Column(db.Integer, db.ForeignKey('persona.perid'))
    rolid = db.Column(db.Integer, db.ForeignKey('rol.rolid'))
    usuname = db.Column(db.String(50), nullable=False)
    usupassword = db.Column(db.String(100), nullable=False)
    usupasswordhash = db.Column(db.String, nullable=False)
    usuemail = db.Column(db.String(100), nullable=False)
    usuimagen = db.Column(db.String(255))
    usudescripcion = db.Column(db.String(255))
    usuestado = db.Column(db.SmallInteger, default=1)
    usuusureg = db.Column(db.String(50))
    usufecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    usuusumod = db.Column(db.String(50))
    usufecmod = db.Column(db.TIMESTAMP)
    
# Relaciones con otras tablas
    # persona = db.relationship('Persona', backref=db.backref('usuarios', lazy=True))
    # rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
    