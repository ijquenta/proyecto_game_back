# Importamos los módulos necesarios de Flask y otras librerías
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  # Para permitir solicitudes CORS (Cross-Origin Resource Sharing)
from flask_restful import Api  # Para crear APIs RESTful
from flask_jwt_extended import JWTManager  # Para la gestión de tokens JWT
from flask_sqlalchemy import SQLAlchemy  # Para interactuar con la base de datos a través de SQLAlchemy
from flask_mail import Mail, Message  # Para el servicio de correo electrónico
from logging.handlers import RotatingFileHandler  # Para el manejo de registros rotativos
from core import configuration  # Importa la configuración central del sistema

# Importamos módulos de JWT
import logging  # Para el registro de eventos
import os

# Importamos las respuestas y rutas del cliente
from client.responses import clientResponses as messages  # Respuestas predefinidas para el cliente
# from client.routes import Routes as routes  # Rutas predefinidas para el cliente

# Importamos las rutas de los diferentes recursos de la aplicación
from routes.usuario_routes import usuario_routes  # Rutas relacionadas con los usuarios
from routes.reporte_routes import reporte_routes  # Rutas relacionadas con los reportes
from routes.rol_routes import rol_routes  # Rutas relacionadas con los roles de usuario
from routes.persona_routes import persona_routes  # Rutas relacionadas con las personas
from routes.materia_routes import materia_routes  # Rutas relacionadas con las materias
from routes.cursomateria_routes import cursomateria_routes  # Rutas relacionadas con los cursos y materias
from routes.nivel_routes import nivel_routes  # Rutas relacionadas con los niveles educativos
from routes.inscripcion_routes import inscripcion_routes  # Rutas relacionadas con las inscripciones
from routes.matricula_routes import matricula_routes  # Rutas relacionadas con las matrículas
from routes.nota_routes import nota_routes  # Rutas relacionadas con las notas
from routes.pago_routes import pago_routes  # Rutas relacionadas con los pagos
from routes.material_routes import material_routes  # Rutas relacionadas con los materiales de estudio
from routes.estudiante_routes import estudiante_routes  # Rutas relacionadas con los estudiantes
from routes.docente_routes import docente_routes  # Rutas relacionadas con los docentes
from routes.contabilidad_routes import contabilidad_routes  # Rutas relacionadas con la contabilidad
from routes.principal_routes import principal_routes  # Rutas principales de la aplicación
from routes.asistencia_routes import asistencia_routes  # Rutas relacionadas con la asistencia

# Define el nombre del archivo de registro y configura el nivel de registro
LOG_FILENAME = 'aplication.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# Obtiene el logger predeterminado y establece su nivel de registro
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Configura un manejador de archivos rotativo para el registro
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=40000000, backupCount=40)
logger.addHandler(handler)

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Configura la clave secreta para la aplicación Flask
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'

# Configura JWT para la gestión de tokens JWT en la aplicación
jwt = JWTManager(app)

# Configura CORS para permitir solicitudes desde otros dominios
CORS(app)

# Configuración del servicio de correo electrónico
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

# Configuración de la base de datos SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Crea una instancia del servicio de correo electrónico
mail = Mail(app)

# Crea una instancia de la clase Api de Flask-RESTful
api = Api(app)

# Crea una instancia de la clase SQLAlchemy para interactuar con la base de datos
db = SQLAlchemy(app)

# Manejador para el error 404 (Página no encontrada)
@app.errorhandler(404)
def page_not_found():
    return messages._404, 404

# Manejador para el error 500 (Error interno del servidor)
@app.errorhandler(500)
def page_not_found():
    return messages._500, 500

# Configura la clave secreta de la aplicación
app.secret_key = configuration.APP_SECRET_KEY


# Apis generales
@app.route('/protected', methods=['GET']) # Api para verificar el decorador token_required
# @token_required 
def protected():
   resp = {"message": "Tienes acceso a esta API"}
   return make_response(jsonify(resp)), 200

 
@app.route('/', methods=['GET']) # Api para verificar si existe una correcta conexión
def index():
   resp = {"message": "Estas en la API de academico_api"}
   return make_response(jsonify(resp)), 200

# Asociación de rutas de API con funciones definidas en otros archivos

# Cada línea invoca una función que define las rutas de API en un archivo específico
usuario_routes(api=api)  # Rutas relacionadas con los usuarios
reporte_routes(api=api)  # Rutas relacionadas con los reportes
rol_routes(api=api)  # Rutas relacionadas con los roles de usuario
persona_routes(api=api)  # Rutas relacionadas con las personas
materia_routes(api=api)  # Rutas relacionadas con las materias
cursomateria_routes(api=api)  # Rutas relacionadas con los cursos y materias
nivel_routes(api=api)  # Rutas relacionadas con los niveles educativos
inscripcion_routes(api=api)  # Rutas relacionadas con las inscripciones
matricula_routes(api=api)  # Rutas relacionadas con las matrículas
nota_routes(api=api)  # Rutas relacionadas con las notas
pago_routes(api=api)  # Rutas relacionadas con los pagos
material_routes(api=api)  # Rutas relacionadas con los materiales de estudio
estudiante_routes(api=api)  # Rutas relacionadas con los estudiantes
docente_routes(api=api)  # Rutas relacionadas con los docentes
contabilidad_routes(api=api)  # Rutas relacionadas con la contabilidad
principal_routes(api=api)  # Rutas principales de la aplicación
asistencia_routes(api=api)  # Rutas relacionadas con la asistencia

# Importamos funciones para registro y login de usuarios
from routes.auth_routes import f_login_usuario, f_register_usuario

@app.route('/academico_api/register', methods=['POST'])
def register_usuario():
    return f_register_usuario()
        
@app.route('/academico_api/login', methods=['POST'])
def login_usuario():
    return f_login_usuario()

# Importamos funciones para subida y descarga de archivos
from routes.subir_archivos_routes import f_upload_file_foto_perfil, f_upload_file_pago, f_upload_file_texto, f_registrarArchivo, f_download_file, f_download_file_texto, f_listarArchivos, f_eliminarArchivo

@app.route('/academico_api/fotoPerfil/upload', methods=['POST'])
def upload_file_foto_perfil():
    f_upload_file_foto_perfil()

@app.route('/academico_api/pago/upload', methods=['POST'])
def upload_file_pago():
    return f_upload_file_pago()

@app.route('/academico_api/texto/upload', methods=['POST'])
def upload_file_texto():
    return f_upload_file_texto()

@app.route('/registrar-archivo', methods=['POST'])
def registrarArchivo():
    return f_registrarArchivo()

@app.route('/academico_api/pago/download/<file_name>')
def download_file(file_name):
    return f_download_file(file_name)

@app.route('/academico_api/texto/download/<file_name>')
def download_file_texto(file_name):
    return f_download_file_texto(file_name)

@app.route('/listar-archivos', methods=['GET'])
def listarArchivos():
    return f_listarArchivos()

@app.route('/eliminar-archivo/<filename>', methods=['DELETE'])
def eliminarArchivo(filename):
    return f_eliminarArchivo(filename)

# Api para Envio de correo 
@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    data = request.get_json()
    destinatario = data.get('destinatario')
    asunto = data.get('asunto')
    mensaje = data.get('mensaje')
    if not destinatario or not asunto or not mensaje:
        return jsonify({'mensaje': 'Faltan datos requeridos'}), 400
    try:
        
        msg = Message(sender = os.environ.get("EMAIL_HOST_USER"), # Crear el mensaje de correo
                      subject=asunto,
                      recipients=[destinatario],
                      body=mensaje)
        mail.send(msg) # Enviar el mensaje de correo
        return jsonify({'mensaje': 'Correo enviado correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error al enviar el correo: {str(e)}'}), 500
    
if __name__ == '__main__':
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print(HOST,PORT, ':3')
	app.run(host=HOST,port=PORT,debug=True)