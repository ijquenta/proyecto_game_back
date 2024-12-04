
from resources.Autenticacion import TokenGenerator, token_required
from flask_bcrypt import Bcrypt

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS # Para permitir solicitudes CORS (Cross-Origin Resource Sharing)
from flask_restful import Api  # Para crear APIs RESTful
from flask_jwt_extended import JWTManager  # Para la gestión de tokens JWT
from flask_sqlalchemy import SQLAlchemy # Para interactuar con la base de datos a través de SQLAlchemy

from datetime import datetime  # Para usar fecha y hora
from logging.handlers import RotatingFileHandler # Para el manejo de registros rotativos
from core import configuration  # Importa la configuración central del sistema
import logging  # Para el registro de eventos
import os  # Para usar funcionalidades del istema operativo

# Importamos las rutas de los diferentes recursos de la aplicación
# from routes.usuario_routes import usuario_routes
from routes.game_routes import game_routes
# from routes.subir_archivos_routes import *

from models.game_model import Usuario, db  # Importamos Usuario

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

# Configuración de la base de datos SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Crea una instancia de la clase Api de Flask-RESTful
api = Api(app)

# Crea una instancia de la clase SQLAlchemy para interactuar con la base de datos
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Configura la clave secreta de la aplicación
app.secret_key = configuration.APP_SECRET_KEY

@app.route('/protected', methods=['GET'])
def protected():
   resp = {"message": "Tienes acceso a esta API"}
   return make_response(jsonify(resp)), 200


@app.route('/', methods=['GET'])
def index():
   resp = {"message": "This is Api Game VR"}
   return make_response(jsonify(resp)), 200

# Invocar las funciones que define las rutas de API
# usuario_routes(api=api)
game_routes(api=api)

@app.route('/v1/register', methods=['POST'])
def f_register_usuario():
    user_data = request.get_json()  # Se recuperan los datos enviados por el método POST

    # Buscamos al usuario con el username
    user = Usuario.query.filter_by(username=user_data['username']).first()

    if not user:
        try:
            user_new = Usuario(
                username=user_data['username'],
                email=user_data['email'],
                # Aquí puedes agregar otros campos si son necesarios
            )

            # Se adiciona el usuario con db.session.add(user_new)
            db.session.add(user_new)
            db.session.commit()  # Se ejecuta la sentencia

            resp = {
                "status": "success",
                "message": "User  successfully registered."
            }
            return make_response(jsonify(resp)), 201
        except Exception as e:
            print(f"Error al confirmar la transacción: {str(e)}")
            # Deshacer los cambios en la base de datos si algo falla.
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
            "message": "User  already exists"
        }
        return make_response(jsonify(resp)), 202

@app.route('/v1/login', methods=['POST'])
def f_login_usuario():
    user_data = request.get_json()
    
    # Verificar si el campo requerido está presente en la solicitud
    if 'username' not in user_data:
        return jsonify({"status": "Error", "message": "Missing email"}), 400

    try:
        # Recuperar el usuario de la base de datos por email
        user = Usuario.query.filter_by(email=user_data['username']).first()

        if user:
            # Generar un token de autenticación (ajusta esto según tu implementación)
            auth_token = TokenGenerator.encode_token(user.id_usuario, user.rol)  # Asegúrate de que el método encode_token esté definido
            resp = {
                "status": "success",
                "message": "Successfully logged in",
                'auth_token': auth_token,
                "usuario": user.id_usuario,
                "rol": user.rol
            }
            return jsonify(resp), 200
        else:
            return jsonify({"status": "Error", "message": "Invalid email"}), 401

    except Exception as e:
        print("Error login user: ", e)
        db.session.rollback()  # Deshacer los cambios si ocurre alguna falla
        return jsonify({
            "status": "Error",
            "message": "Internal server error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	app.run(host=HOST, port=PORT,debug=True)