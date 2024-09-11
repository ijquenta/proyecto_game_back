
from resources.Autenticacion import TokenGenerator, token_required
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS # Para permitir solicitudes CORS (Cross-Origin Resource Sharing)
from flask_restful import Api  # Para crear APIs RESTful
from flask_jwt_extended import JWTManager  # Para la gestión de tokens JWT
from flask_sqlalchemy import SQLAlchemy # Para interactuar con la base de datos a través de SQLAlchemy
from flask_mail import Mail, Message  # Para el servicio de correo electrónico

from datetime import datetime  # Para usar fecha y hora
from logging.handlers import RotatingFileHandler # Para el manejo de registros rotativos
from core import configuration  # Importa la configuración central del sistema
import logging  # Para el registro de eventos
import os  # Para usar funcionalidades del istema operativo

# Respuestas predefinidas para el cliente
from client.responses import clientResponses as messages

# Importamos las rutas de los diferentes recursos de la aplicación
from routes.usuario_routes import usuario_routes
from routes.reporte_routes import reporte_routes
from routes.rol_routes import rol_routes
from routes.persona_routes import persona_routes
from routes.materia_routes import materia_routes
from routes.cursomateria_routes import cursomateria_routes
from routes.nivel_routes import nivel_routes
from routes.inscripcion_routes import inscripcion_routes
from routes.matricula_routes import matricula_routes
from routes.nota_routes import nota_routes
from routes.pago_routes import pago_routes
from routes.material_routes import material_routes
from routes.estudiante_routes import estudiante_routes
from routes.docente_routes import docente_routes
from routes.contabilidad_routes import contabilidad_routes
from routes.principal_routes import principal_routes
from routes.asistencia_routes import asistencia_routes
from routes.permiso_routes import permiso_routes
from routes.operacion_routes import operacion_routes
from routes.acceso_routes import acceso_routes
from routes.menu_routes import menu_routes
from routes.tipoIcono_routes import tipoIcono_routes
from routes.submenu_routes import submenu_routes
from routes.texto_routes import texto_routes
from routes.horario_routes import horario_routes
# from routes.auth_routes import f_login_usuario
from routes.subir_archivos_routes import *

from models.usuario_model import Usuario, db  # Importamos Usuario

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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Crea una instancia del servicio de correo electrónico
mail = Mail(app)

# Crea una instancia de la clase Api de Flask-RESTful
api = Api(app)

# Crea una instancia de la clase SQLAlchemy para interactuar con la base de datos
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Configura la clave secreta de la aplicación
app.secret_key = configuration.APP_SECRET_KEY

# from flask_swagger_ui import get_swaggerui_blueprint

# SWAGGER_URL="/swagger"
# API_URL="/static/swagger.json"

# swagger_ui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': 'Access API'
#     }
# )
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Api para verificar el decorador token_required
@app.route('/protected', methods=['GET'])
# @token_required
def protected():
   resp = {"message": "Tienes acceso a esta API"}
   return make_response(jsonify(resp)), 200


# Api para verificar si existe una correcta conexión
@app.route('/', methods=['GET'])
def index():
   resp = {"message": "Estas en la API de academico_api"}
   return make_response(jsonify(resp)), 200

# Asociación de rutas de API con funciones definidas en otros archivos

# Invocar las funciones que define las rutas de API
usuario_routes(api=api, mail=mail)
reporte_routes(api=api)
rol_routes(api=api)
persona_routes(api=api)
materia_routes(api=api)
cursomateria_routes(api=api)
nivel_routes(api=api)
inscripcion_routes(api=api)
matricula_routes(api=api)
nota_routes(api=api)
pago_routes(api=api)
material_routes(api=api)
estudiante_routes(api=api)
docente_routes(api=api)
contabilidad_routes(api=api)
principal_routes(api=api)
asistencia_routes(api=api)
permiso_routes(api=api)
operacion_routes(api=api)
acceso_routes(api=api)
menu_routes(api=api)
tipoIcono_routes(api=api)
submenu_routes(api=api)
texto_routes(api=api)
horario_routes(api=api)

"""
Apis para inicar sesion, registrarse y confirmar correo.
"""
@app.route('/academico_api/register', methods=['POST'])
def f_register_usuario():  # Función para regitrar un usuario

    user_data = request.get_json()  # se recupera los datos enviados por el método post
    # buscamos al usuario con el usuname (nombre de usuario)
    user = Usuario.query.filter_by(usuname=user_data['usuname']).first()

    if not user:
        try:
            # Se genera la contraseña con el hash, para mayor seguridad
            hashed_password = bcrypt.generate_password_hash(user_data['usupassword']).decode('utf-8')

            user_new = Usuario(
                usuname=user_data['usuname'],
                usupassword=hashed_password,
                usupasswordhash=hashed_password,
                perid=user_data['perid'],
                rolid=user_data['rolid'],
                usuemail=user_data['usuemail'],
                usudescripcion=user_data['usudescripcion'],
                usuusureg=user_data['usuusureg'],
                usuusumod=user_data['usuusureg'],
                usufecreg=datetime.now(),
                usufecmod=datetime.now(),
                usuestado=user_data['usuestado']
            )

            # Se adiciona el usuario con db.session.add(usuario_nuevo)
            db.session.add(user_new)
            db.session.commit()  # Se ejecuta la sentencia
            # Genera el token de confirmación para enviar por email
            confirmation_token = TokenGenerator.generate_confirmation_token(
                user_new.usuid, user_new.rolid)  # en el token se enviara el usuid y el rolid

            # Envía el correo electrónico de confirmación
            # se envia a la siguiente función el cual enviara el email enviar_correo_verificar
            if enviar_correo_verificar(user_data['usuemail'], confirmation_token):
                resp = {
                    "status": "success",
                    "message": "User successfully registered. Confirmation email sent."
                }
                return make_response(jsonify(resp)), 201
            else:
                resp = {
                    "status": "Error",
                    "message": "Error occurred while sending confirmation email"
                }
                return make_response(jsonify(resp)), 500
        except Exception as e:
            print(f"Error al confirmar la transacción: {str(e)}")
            # Deshacer los cambios en la base de  datos si algo falla.
            # Revertir los cambios en la base de datos si ocurre un error de durante la transaccion
            db.session.rollback()
            resp = {
                "status": "Error",
                "message": "Error occurred, user registration failed",
                "error": str(e)
            }
            return make_response(jsonify(resp)), 500
    else:
        resp = {
            "status": "error",
            "message": "User already exists"
        }
        return make_response(jsonify(resp)), 202

from models.rol_model import Rol
@app.route('/academico_api/login', methods=['POST'])
def f_login_usuario():
    user_data = request.get_json()
    # Verificar si los campos requeridos están presentes en la solicitud
    if 'usuname' not in user_data or 'usupassword' not in user_data:
        return jsonify({"status": "Error", "message": "Missing username or password"}), 400

    try:  # recuperar el usuario de la base de datos
        user = Usuario.query.filter_by(usuname=user_data['usuname']).first()

        if user:
            if not user.usuconfirmado:  # Verificar si el usuario está confirmado por correo electrónico
                return jsonify({"status": "Error", "message": "Email not confirmed. Please confirm your email before logging in."}), 401

            # Verificar si la contraseña es correcta
            if bcrypt.check_password_hash(user.usupassword, user_data['usupassword']):
                rol = Rol.query.get(user.rolid)
                auth_token = TokenGenerator.encode_token(
                    user.usuid, rol.rolnombre)
                resp = {
                    "status": "success",
                    "message": "Successfully logged in",
                    'auth_token': auth_token,
                    "usuario": user.usuid,
                    "rol": rol.rolnombre,
                }
                return jsonify(resp), 200
            else:
                return jsonify({"status": "Error", "message": "Invalid username or password"}), 401
        else:
            return jsonify({"status": "Error", "message": "Invalid username or password"}), 401

    except Exception as e:
        print("Error login user: ", e)
        db.session.rollback()  # Deshacer los cambios si ocurre alguna falla
        return jsonify({
            "status": "Error",
            "message": "Internal server error",
            "error": str(e)
        }), 500

from models.usuario_model import Usuario, db
@app.route("/academico_api/confirm-email", methods=['POST'])
def confirm_email():
    token = request.get_json().get('token')  # obtenemos el token
    print(token)
    if not token:
        return jsonify({"status": "error", "message": "No se proporcionó ningún token de confirmación."}), 400

    # Confirma el token y obtiene el email
    email = TokenGenerator.confirm_token(token)
    if email is None:
        return jsonify({"status": "error", "message": "El enlace de confirmación es inválido o ha expirado."}), 400

    usuid, rolid = TokenGenerator.extract_user_info_from_token(
        token)  # Obtiene usuid y rolid del token
    print("usuario: ", usuid)
    try:
        user = Usuario.query.filter_by(usuid=usuid).first()
        print("usuario encontrado",user)
        if user is None:
            return jsonify({"status": "error", "message": "Usuario no encontrado."}), 404

        if user.usuconfirmado:
            return jsonify({"status": "already_confirmed", "message": "Tu cuenta ya ha sido confirmada previamente."}), 400

        user.usuconfirmado = 1
        user.usuconfirmadofecreg = datetime.now()
        db.session.commit()

        return jsonify({"status": "success", "message": "¡Has confirmado tu cuenta exitosamente! ¡Gracias!"}), 200
    except Exception as e:
        print(f"Error al confirmar la transacción: {str(e)}")
        db.session.rollback()  # Revertir la transacción en caso de error
        return jsonify({
            "status": "error",
            "message": "Ocurrió un error al confirmar tu cuenta: {}".format(str(e))
        }), 500



# Importamos funciones para subida y descarga de archivos
@app.route('/academico_api/profilePhoto/upload', methods=['POST'])
@token_required
def upload_file_foto_perfil():
    return f_upload_file_foto_perfil(request)


@app.route('/academico_api/profilePhoto/delete', methods=['POST'])
@token_required
def delete_file_foto_perfil():
    return f_delete_foto_perfil()


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

        msg = Message(sender=os.environ.get("EMAIL_HOST_USER"),  # Crear el mensaje de correo
                      subject=asunto,
                      recipients=[destinatario],
                      body=mensaje)
        mail.send(msg)  # Enviar el mensaje de correo
        return jsonify({'mensaje': 'Correo enviado correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error al enviar el correo: {str(e)}'}), 500


def enviar_correo_verificar(destinatario, confirmation_token):
    try:
        msg = Message(
            "CONFIRMACIÓN DE REGISTRO DE USUARIO",
            sender=os.environ.get("EMAIL_HOST_USER"),
            recipients=[destinatario],
        )
        confirmation_link = f"http://localhost:4200/verified?token={confirmation_token}"
        msg.html = f"""
        <html>
        <body>
            <p>Para confirmar su registro, haga clic en el botón siguiente:</p>
            <a href="{confirmation_link}" style="display: inline-block; padding: 10px 20px; font-size: 16px; font-family: Arial, sans-serif; color: white; background-color: #28a745; text-decoration: none; border-radius: 5px;">
                Activar registro de usuario
            </a>
            <p>Si no realizó esta solicitud, simplemente ignore este correo electrónico y no se realizarán cambios.</p>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        return False


# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'

# swagger_ui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Access API"
#     }
# )

# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	app.run(host=HOST, port=PORT,debug=True)