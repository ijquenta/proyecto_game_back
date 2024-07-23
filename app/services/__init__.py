# import os
# from flask import Flask
# from flask_cors import CORS
# from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail, Message  # Para el servicio de correo electrónico

# # Crea una instancia de la aplicación Flask
# app = Flask(__name__)

# # Configura la clave secreta para la aplicación Flask
# app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'

# # Configura JWT para la gestión de tokens JWT en la aplicación
# # jwt = JWTManager(app)

# # Configura CORS para permitir solicitudes desde otros dominios
# CORS(app)

# # Configuración del servicio de correo electrónico
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
# app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
# app.config["MAIL_USE_TLS"] = False
# app.config["MAIL_USE_SSL"] = True

# # Configuración de la base de datos SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# # Crea una instancia del servicio de correo electrónico
# mail = Mail(app)

# # Crea una instancia de la clase Api de Flask-RESTful
# api = Api(app)

# # Crea una instancia de la clase SQLAlchemy para interactuar con la base de datos
# db = SQLAlchemy(app)
# Crea una instancia de SQLAlchemy
db = SQLAlchemy()

# Ahora `db` está definido y puede ser importado desde otros archivos dentro de la carpeta `models`
