from flask import Flask, request, jsonify, make_response, send_file, session
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy # Base de datos
from flask_mail import Mail, Message # importamos para el servicio de correo
from logging.handlers import RotatingFileHandler
from core import configuration
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
# import jwt
import logging
import os # impotamos para obtener las variables de entorno
import random
import string
# Client
from client.responses import clientResponses as messages
from client.routes import Routes as routes
# Models
from model.pago_model import modelPago
# Resources
import resources.Reportes as Report
# import resources.Usuario as Usuario
import resources.Autenticacion as Autenticacion
import resources.Rol as Rol
import resources.Estudiante as Estudiante
import resources.Docente as Docente
import resources.Asistencia as Asistencia
import services.nivel_service as NivelService

LOG_FILENAME = 'aplication.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=40000000, backupCount=40)
logger.addHandler(handler)
app = Flask(__name__)
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'
jwt = JWTManager(app)
CORS(app)
# app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mail = Mail(app)
api = Api(app)
db = SQLAlchemy(app)


@app.errorhandler(404)
def page_not_found(error):
    return messages._404, 404

@app.errorhandler(500)
def page_not_found(error):
    return messages._500, 500

api = Api(app)
app.secret_key = configuration.APP_SECRET_KEY

# API Usuarios
from routes.usuario import usuario_routes
usuario_routes(api=api)
# Reporte Prueba
api.add_resource(Report.rptTotalesSigma, routes.rptTotalesSigma)
# Roles
api.add_resource(Rol.ListarRoles, routes.listarRoles)
api.add_resource(Rol.GestionarRol, routes.gestionarRol)
#Persona
from routes.persona import persona_routes
persona_routes(api=api)
# Materia
from routes.materia import materia_routes
materia_routes(api=api)
# Curso - Materia
from routes.cursomateria import cursomateria_routes
cursomateria_routes(api=api)
# Nivel
from routes.nivel import nivel_routes
nivel_routes(api=api)
# Inscripción
from routes.inscripcion import inscripcion_routes
inscripcion_routes(api=api)
# Matricula
from routes.matricula import matricula_routes
matricula_routes(api=api)
# Estudiante
api.add_resource(Estudiante.ListarEstudiante, routes.listarEstudiante)
api.add_resource(Estudiante.ObtenerMateriasInscritas, routes.obtenerMateriasInscritas)
# Docente
api.add_resource(Docente.ListarDocente, routes.listarDocente)
api.add_resource(Docente.ObtenerMateriasAsignadas, routes.obtenerMateriasAsignadas)
api.add_resource(Docente.ListarMateriaEstudianteCurso, routes.listarMateriaEstudianteCurso)
# Nota
from routes.nota import nota_routes
nota_routes(api=api)
# Pago
from routes.pago import pago_routes
pago_routes(api=api)
# Asistencia
api.add_resource(Asistencia.ListarAsistencia, routes.listarAsistencia)
# Material
from routes.material import material_routes
material_routes(api=api)


# from model.persona import Persona as Persona
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
# from model.rol import Rol as Rol
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
# from model.usuario import Usuario
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

from resources.Autenticacion import TokenGenerator

import jwt
def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing",
                    "error": "Unauthorized"
                }, 401
            try:
                data=jwt.decode(token, os.environ.get("APP_SECRET_KEY"), algorithms=["HS256"])
                # data=TokenGenerator.decode_token(token)
                current_user=Usuario().get_by_id(data["sub"])
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

@app.route('/academico_api/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    user = Usuario.query.filter_by(usuname = user_data['usuname']).first()
    if not user:
        try: 
            hashed_password = generate_password_hash(user_data['usupassword'])
            user_new = Usuario(usuname = user_data['usuname'], usupassword = hashed_password, perid = user_data['perid'], rolid = user_data['rolid'])
            db.session.add(user_new)
            db.session.commit()
            resp = {
                "status":"success",
                "message":"User successfully registered",
            }
            return make_response(jsonify(resp)),201
        except Exception as e:
            # print(e)
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
        
@app.route('/academico_api/login', methods = ['POST'])
def post():
    user_data = request.get_json()
    try:
        user = Usuario.query.filter_by(usuname = user_data['usuname']).first()
        if user and check_password_hash(user.usupassword, user_data['usupassword']) == True:
            rol = Rol.query.get(user.rolid)
            auth_token = TokenGenerator.encode_token(user.usuid, rol.rolnombre)
            resp = {
                "status":"succes",
                "message" :"Successfully logged in",
                'auth_token':auth_token,
                "usuario": user.usuid,
                "rol": rol.rolnombre,
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

@app.route('/protected', methods=['GET'])
# @token_required 
def protected():
   resp = {"message": "Tienes acceso a esta API"}
   return make_response(jsonify(resp)), 200

 


EXTENSIONS_PDF = {'pdf'}
EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_PDF

def allowed_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_IMG

def stringAleatorio(length=10):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

# import urllib.request
# from werkzeug.utils import secure_filename # pip install Werkzeug
# import os
# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# @app.route('/academico_api/fotoPerfil/upload', methods=['POST'])
# def upload_file():
#     if 'files[]' not in request.files:
#         resp=jsonify({
#             "message": 'No hay archivo en la respuesta',
#             "status": 'failed'
#         })
#         resp.status_code = 400
#         return resp
#     files = request.files.getlist('files[]')
#     errors = {}
#     success = False
#     for file in files: 
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             success = True
#         else: 
#             resp = jsonify({
#                 "message": 'Tipo de archivo no es permitido.',
#                 "status": 'failed'
#             })
#             return resp
#     if success and errors:
#         errors['message'] = 'Archivos subidos correctamente'
#         errors['status'] = 'failed'
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp
#     if success: 
#         resp = jsonify({
#             "message": 'Archivo subido correctamente',
#             "status": 'success'
#         })
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp


@app.route('/academico_api/fotoPerfil/upload', methods=['POST'])
def upload_file_foto_perfil():
    if 'files[]' not in request.files:
        return jsonify({"message": 'No hay imagenes en la solicitud', "status": 'failed'}), 400
    
    files = request.files.getlist('files[]')
    errors = []
    success = False
    
    for file in files:
        if file and allowed_file_img(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'files_fotoperfil')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            # nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, filename)
            file.save(upload_path)
            success = True
        else:
            errors.append({'filename': file.filename, 'message': 'Tipo de archivo no permitido.'})

    if success:
        if errors:
            status_code = 207  # Código de estado HTTP para respuesta parcial
            message = 'Algunos archivos no se pudieron subir.'
        else:
            status_code = 201
            message = 'Todos los archivos subidos correctamente.'
    else:
        status_code = 400
        message = 'Ningún archivo subido correctamente.'

    return jsonify({"message": message, "errors": errors, "status": 'success' if success else 'failed'}), status_code


@app.route('/academico_api/pago/upload', methods=['POST'])
def upload_file_pago():
    if 'files[]' not in request.files:
        return jsonify({"message": 'No hay archivos en la solicitud', "status": 'failed'}), 400
    
    files = request.files.getlist('files[]')
    errors = []
    success = False
    
    for file in files:
        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'files_pago')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            # nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, filename)

            file.save(upload_path)
            success = True
        else:
            errors.append({'filename': file.filename, 'message': 'Tipo de archivo no permitido.'})

    if success:
        if errors:
            status_code = 207  # Código de estado HTTP para respuesta parcial
            message = 'Algunos archivos no se pudieron subir.'
        else:
            status_code = 201
            message = 'Todos los archivos subidos correctamente.'
    else:
        status_code = 400
        message = 'Ningún archivo subido correctamente.'

    return jsonify({"message": message, "errors": errors, "status": 'success' if success else 'failed'}), status_code

@app.route('/academico_api/texto/upload', methods=['POST'])
def upload_file_texto():
    if 'files[]' not in request.files:
        return jsonify({"message": 'No hay archivos en la solicitud', "status": 'failed'}), 400
    
    files = request.files.getlist('files[]')
    errors = []
    success = False
    
    for file in files:
        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'files_texto')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            # nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, filename)

            file.save(upload_path)
            success = True
        else:
            errors.append({'filename': file.filename, 'message': 'Tipo de archivo no permitido.'})

    if success:
        if errors:
            status_code = 207  # Código de estado HTTP para respuesta parcial
            message = 'Algunos archivos no se pudieron subir.'
        else:
            status_code = 201
            message = 'Todos los archivos subidos correctamente.'
    else:
        status_code = 400
        message = 'Ningún archivo subido correctamente.'

    return jsonify({"message": message, "errors": errors, "status": 'success' if success else 'failed'}), status_code

@app.route('/academico_api/pago/download/<file_name>')
def download_file(file_name):
    archivo_path = 'static/files_pago/' + file_name
    return send_file(archivo_path, as_attachment=True)

@app.route('/academico_api/texto/download/<file_name>')
def download_file_texto(file_name):
    archivo_path = 'static/files_texto/' + file_name
    return send_file(archivo_path, as_attachment=True)

@app.route('/registrar-archivo', methods=['POST'])
def registrarArchivo():
    try:
        if 'archivo' not in request.files:
            raise ValueError("No se proporcionó ningún archivo en la solicitud.")

        file = request.files['archivo']

        if file.filename == '':
            raise ValueError("Nombre de archivo vacío.")

        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'archivos')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, nuevo_nombre_file)

            file.save(upload_path)

            resp = {
                "status": "success",
                "message": "Archivo subido correctamente",
                "filename": nuevo_nombre_file  # Puedes enviar el nuevo nombre del archivo si es necesario
            }
            return jsonify(resp), 200
        else:
            raise ValueError("Tipo de archivo no permitido.")

    except Exception as e:
        resp = {
            "status": "error",
            "message": f"Error al subir el archivo: {str(e)}"
        }
        return jsonify(resp), 500

@app.route('/listar-archivos', methods=['GET'])
def listarArchivos():
    basepath = os.path.dirname(__file__)
    upload_directory = os.path.join(basepath, 'static', 'archivos')

    if not os.path.exists(upload_directory):
        return jsonify({"archivos": []})

    archivos = os.listdir(upload_directory)
    return jsonify({"archivos": archivos})

@app.route('/eliminar-archivo/<filename>', methods=['DELETE'])
def eliminarArchivo(filename):
    try:
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, 'static', 'archivos')

        file_path = os.path.join(upload_directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            resp = {
                "status": "success",
                "message": f"Archivo {filename} eliminado correctamente"
            }
            return jsonify(resp), 200
        else:
            raise FileNotFoundError(f"El archivo {filename} no existe.")

    except Exception as e:
        resp = {
            "status": "error",
            "message": f"Error al eliminar el archivo: {str(e)}"
        }
        return jsonify(resp), 500

@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    data = request.get_json()
    destinatario = data.get('destinatario')
    asunto = data.get('asunto')
    mensaje = data.get('mensaje')
    if not destinatario or not asunto or not mensaje:
        return jsonify({'mensaje': 'Faltan datos requeridos'}), 400
    try:
        # Crear el mensaje de correo
        msg = Message(sender = os.environ.get("EMAIL_HOST_USER"),
                      subject=asunto,
                      recipients=[destinatario],
                      body=mensaje)
        # Enviar el mensaje de correo
        mail.send(msg)
        return jsonify({'mensaje': 'Correo enviado correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error al enviar el correo: {str(e)}'}), 500
    

    
if __name__ == '__main__':
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print(HOST,PORT, ':3')
	app.run(host=HOST,port=PORT,debug=True)