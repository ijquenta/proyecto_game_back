from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from core import configuration
from services.persona_service import *
from model.user import User, db


app = Flask(__name__) # Aplicación Flask
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'
jwt = JWTManager(app)

from flask import Flask,request,jsonify,make_response
from werkzeug.security import generate_password_hash
# from resources.Autenticacion import User, db,check_password_hash, encode_token, token_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

CORS(app)

    
api = Api(app)

app.secret_key = configuration.APP_SECRET_KEY
# Configuración de la base de datos

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
    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'))
    rolid = db.Column(db.Integer, db.ForeignKey('academico.rol.rolid'))
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
    
    persona = db.relationship('Persona', backref=db.backref('usuarios', lazy=True))
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
    
def encode_token(user_id, user_rol):
    print("encode_token: Datos recibidos: ", user_id, user_rol)
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0,minutes=60,seconds=0), # Expiración del token
        'iat': datetime.utcnow(),
        'sub': user_id,
        'rol': user_rol 
    }
    print("Payload: ", payload)
    token = jwt.encode(payload, configuration.APP_SECRET_KEY, algorithm='HS256')
    print("Token: ", token)
    print("Token Generado: ", token.decode('utf-8'))
    return token.decode('utf-8')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print("request.headers: ", request.headers)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            # print("Este es el token: ", token)
        if not token:
            return {
                "message": "Authentication Token is missing",
                "error": "Unauthorized"
            }, 401
        try:
            # print("SECRET_KEY_1: ", app.secret_key)
            # print("SECRET_KEY_2: ", app.config["SECRET_KEY"])
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            # print("data decode token: ", data)
            current_user=Usuario().get_by_id(data["sub"])
            print("usuario_actual", current_user)
            if current_user is None:
                return {
                "message": "Invalid Authentication token",
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "An error Occured",
                "error": str(e)
            }, 401
        return f(*args, **kwargs)
    return decorated


if __name__ == '__main__':
	#Base.metadata.create_all(engine)
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print (HOST,PORT, ':3')
	app.run(host=HOST,port=PORT,debug=True)
