from flask_cors import CORS
from flask import Flask, session, jsonify, request
# from flask_restx import Api, Resource
from flask_restful import Api
from flask_jwt_extended import JWTManager
from logging.handlers import RotatingFileHandler
from core import configuration
import logging
import traceback
import os

from client.responses import clientResponses as messages
from client.routes import Routes as routes

# import resources.resources as resources
# import resources.BenSocial as BenSocial
import resources.Persona as Persona
import resources.Reportes as Report
import resources.Usuario as Usuario
import resources.Materia as Materia
import resources.Curso as Curso
import resources.Nivel as Nivel
import resources.Autenticacion as Autenticacion
import services.nivel_service as NivelService
import resources.Inscripcion as Inscripcion
import resources.Matricula as Matricula

from core.database import Base, session_db, engine
from web.wsrrhh_service import *


# Librerias para para JWT (Json Web Token)
# requests: acceder datos enviados del por el cliente en una solicitud http.
# jsonify: es una función para convertir objetvos de Python en repuestas JSON al cliente.
# make_responde: se utlizara para crear una respuesta HTTP personalizada.
# reder_template: se tuliza para renderizar planillas HTML.
# session: permite almacenar datos del usuario en una sesión persistente entre solicitudes HTTP.
# jwt. es una biblioteca para trabajnar con tokens JWT, permite crear firmar y verificar tokens JWT, que son utiles para la autenticación y autorización en aplicaciones web.
# datetime: se utilizan para trabajar con fecha y tiempos.
# wraps: es un decorador en Python, se utiliza para mantener infomación de metadatos de una función, como su nombre y su documentación.
# from flask import Flask, request, jsonify, make_response, render_template, session
# import jwt
# from datetime import datetime, timedelta
# from functools import wraps
# importar para JWT

LOG_FILENAME = 'aplication.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=40000000, backupCount=40)
logger.addHandler(handler)


app = Flask(__name__) # Aplicación Flask
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'

# def token_required(func): # Esta es un función decoradora llamada "token_requerid". Toma una función func como argumentos.
# 	# decorator factory which invoks update_wrapper() method and passes decorated function as an argument
# 	@wraps(func) # Este decarorador sirve para preservar los metadatos de la función original 
# 	def decorated(*args, **kwargs): # esta fución anidad toma cualquier número de argumentos y palabras clave (*args y **kwargs)
# 		token = request.args.get('token') # se intenta obtener el token JWT de los argumentos de la solicitud HTTP.
# 		if not token: # Si no encuentra el token en los argumentso de la solicitud, retorna una alerta.
# 			return jsonify({'Alert!':'Token is missing!'}), 401 #Se retorna el http 401 (No autorizando)
# 		try: 
# 			payload = jwt.decode(token, app.config['SECRET_KEY']) # intenta decodificar el token JWT utlizando una calve sercrea almacenada en la configuración de la aplicación
# 															   # Si tien exito, la carga útil (payload) del token se malcenará en la variable payload
# 			# You can use the JWT errs in exception
# 		# except jwt.InvalidTokenError:
# 		# 	return 'Invalid token. Please log in again.'
# 		except: # Si ocurre una exception durante la decodifación del token (por ejemplo, si el oten es invalido)
# 			return jsonify({'Alert':'Invalid Token'}), 403 # Devuelve una respuesta JSON que idica que el token es invalido con el codigo de estado 403 (Prohibido)
# 		return func(*args, **kwargs) # Si el token es valido, la función decorada original (func) se llama conlos mismo argumnetos y palabras clave que recibio
# 	return decorated # La función deracdora devuelve la función anidad "decorated", que se encargará de la autenticación antes de llamar a la función original

# @app.route('/')
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#     	 return 'Logged in currently'
	
# @app.route('/public')
# def public():
# 	return 'For Public'

# @app.route('/auth')
# @token_required
# def auth():
# 	return 'JWT is verified. Welcome to your dashboard'
	


# Login
# @app.route('/login', methods=['POST'])
# def login():
#     if request.form['username'] =='ijquenta' and request.form['password'] == '123456':
#         session['logged_in'] = True

#         token = jwt.encode({
#             'user': request.form['username'],
#             # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
#             'expiration': str(datetime.utcnow() + timedelta(seconds=60))
#         },
#             app.config['SECRET_KEY'])
#         return jsonify({'token': token.decode('utf-8')})
#     else:
#         return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


# @app.route('/logout', methods=['POST'])
# def logout():
#     pass

CORS(app)

@app.errorhandler(404)
def page_not_found(error):
    return messages._404, 404

@app.errorhandler(500)
def page_not_found(error):
    return messages._500, 500
    
api = Api(app)

app.secret_key = configuration.APP_SECRET_KEY

# api.add_resource(resources.Index, routes.index)
# api.add_resource(resources.Protected, routes.protected)

# api.add_resource(Autenticacion.Login, routes.login)
# api.add_resource(Autenticacion.Verify, routes.verify)


# Autenticacion
api.add_resource(Autenticacion.UserLogin, routes.login2)
api.add_resource(Autenticacion.RegisterUser, routes.register2)


# API Usuarios
api.add_resource(Persona.ListarUsuarios, routes.listaUsuarios)

# Reporte Prueba
api.add_resource(Report.rptTotalesSigma, routes.rptTotalesSigma)

# Roles
api.add_resource(Usuario.ListarRoles, routes.listarRoles)
api.add_resource(Usuario.CrearRol, routes.crearRol)
# api.add_resource(Usuario.Login, routes.login)
api.add_resource(Usuario.ModificarRol, routes.modificarRol)
api.add_resource(Usuario.EliminarRol, routes.eliminarRol)

#Persona
api.add_resource(Usuario.ListarPersona, routes.listarPersona)

# Materia
api.add_resource(Materia.ListarMateria, routes.listarMateria)
api.add_resource(Materia.EliminarMateria, routes.eliminarMateria)
api.add_resource(Materia.InsertarMateria, routes.insertarMateria)
api.add_resource(Materia.ModificarMateria, routes.modificarMateria)


# Curso - Materia
api.add_resource(Curso.ListarCursoMateria, routes.listarCursoMateria)
api.add_resource(Curso.EliminarCursoMateria, routes.eliminarCursoMateria)
api.add_resource(Curso.InsertarCursoMateria, routes.insertarCursoMateria)
api.add_resource(Curso.ModificarCursoMateria, routes.modificarCursoMateria)
api.add_resource(Curso.TipoRol, routes.tipoRol)


# Combo
api.add_resource(Curso.ListaCursoCombo, routes.listaCursoCombo)
api.add_resource(Materia.ListaMateriaCombo, routes.listaMateriaCombo)
api.add_resource(Curso.ListaPersonaDocenteCombo, routes.listaPersonaDocenteCombo)


# Nivel
api.add_resource(Nivel.ListarNivel, routes.listarNivel)
api.add_resource(Nivel.InsertarNivel, routes.insertarNivel)
api.add_resource(Nivel.ModificarNivel, routes.modificarNivel)
api.add_resource(Nivel.EliminarNivel, routes.eliminarNivel)


# Inscripción
api.add_resource(Inscripcion.ListarInscripcion, routes.listarInscripcion)
api.add_resource(Inscripcion.InsertarInscripcion, routes.insertarInscripcion)
api.add_resource(Inscripcion.ModificarInscripcion, routes.modificarInscripcion)
api.add_resource(Inscripcion.EliminarInscripcion, routes.eliminarInscripcion)
api.add_resource(Inscripcion.ObtenerCursoMateria, routes.obtenerCursoMateria)
api.add_resource(Inscripcion.ListarComboCursoMateria, routes.listarComboCursoMateria)
api.add_resource(Inscripcion.ListarComboMatricula, routes.listarComboMatricula)


# Matricula
api.add_resource(Matricula.ListarMatricula, routes.listarMatricula)
api.add_resource(Matricula.InsertarMatricula, routes.insertarMatricula)
api.add_resource(Matricula.ModificarMatricula, routes.modificarMatricula)
api.add_resource(Matricula.EliminarMatricula, routes.eliminarMatricula)






 
# JWT
# from flask_jwt_extended import create_access_token

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')
    
#     user = User.query.filter_by(username=username).first()
    
#     if user and check_password_hash(user.password, password):
#         access_token = create_access_token(identity=username)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify(message='Credenciales inválidas'), 401

from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    date_registered = db.Column(db.DateTime, default = datetime.utcnow())


def encode_token(user_id, user_email):
    print("encode_token: Datos recibidos: ", user_id, user_email)
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0,seconds=30),
        'iat': datetime.utcnow(),
        'sub': user_id,
        'email': user_email 
    }
    print("Payload: ", payload)
    token = jwt.encode(payload, configuration.APP_SECRET_KEY, algorithm='HS256')
    print("Token Generado: ", token.decode('utf-8'))
    return token.decode('utf-8')


from flask import Flask,request,jsonify,make_response
from werkzeug.security import generate_password_hash

@app.route('/academico_api/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    print("Datos recuperados:", user_data)
    
    user = User.query.filter_by(email = user_data['email']).first()
    print("Busqueda de usuario: ",user)
    if not user:
        try: 
            hashed_password = generate_password_hash(user_data['password'])
            print("Se resguarda el password: ", hashed_password)
            user_new = User(email = user_data['email'], password = hashed_password)
            print("Se crea el usuario para adicionar en la BD: ", user_new.email, user_new.password)
            db.session.add(user_new)
            db.session.commit()
            resp = {
                "status":"success",
                "message":"User successfully registered",
            }
            return make_response(jsonify(resp)),201

        except Exception as e:
            print(e)
            resp = {
                "status" :"Error",
                "message" :" Error occured, user registration failed"
            }
            return make_response(jsonify(resp)),401
    else:
        resp = {
            "status":"error",
            "message":"User already exists"
        }
        return make_response(jsonify(resp)),202
        
@app.route('/academico_api/login',methods = ['POST'])
def post():
    user_data = request.get_json()
    print("Se reciben los datos: ", user_data)
    try:
        user = User.query.filter_by(email = user_data['email']).first()
        print("Obtenermos los datos del usuario: ", user)
        if user and check_password_hash(user.password,user_data['password'])==True:
            print("Usuario verificado")
            auth_token = encode_token(user.id, user.email)
            print("Auth_Token: ", auth_token)
            resp = {
                "status":"succes",
                "message" :"Successfully logged in",
                'auth_token':auth_token,
                "usuario": user.id,
                "email": user.email,
            }
            return make_response(jsonify(resp)),200
        else:
            resp ={
                "status":"Error",
                "message":"User does not exist"
            }
            return make_response(jsonify(resp)), 404

    except Exception as e:
        print(e)
        resp = {
            "Status":"error",
                "Message":"User login failed"
        }
        return make_response(jsonify(resp)), 404
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print("request.headers: ", request.headers)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            print("Este es el token: ", token)
        if not token:
            return {
                "message": "Authentication Token is missing",
                "error": "Unauthorized"
            }, 401
        try:
            print("SECRET_KEY_1: ", app.secret_key)
            print("SECRET_KEY_2: ", app.config["SECRET_KEY"])
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            print("data decode token: ", data)
            current_user=User().get_by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token",
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "An error Occured",
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/protected', methods=['GET'])
@token_required 
def protected():
   print("Proteccion")  
   resp = {"message":"Tienes acceso a esta API"}   
   return make_response(jsonify(resp)), 404



if __name__ == '__main__':
	#Base.metadata.create_all(engine)
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print (HOST,PORT, ':3')
	app.run(host=HOST,port=PORT,debug=True)