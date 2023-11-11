from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
# from core.auth import require_token
from http import HTTPStatus
from services.beneficio_service import *
from services.usuario_service import *
from core.auth import *

#import services.beneficio_service as beneficio



# parseLogin = reqparse.RequestParser()
# parseLogin.add_argument('usuario', type=str, help = 'Debe elegir un usuario', required = True)
# parseLogin.add_argument('contrasenia', type=str, help = 'Debe elegir una contraseña', required = True)
# class Login(Resource):
#   def post(self):
#       data = parseLogin.parse_args()
#       print("data->",data)
#       if data.usuario == "ijquenta" and data.contrasenia == "123456":
#          return write_token(data)
#       else:
#          response =jsonify({"message": "Usuario no encontrado"})
#          response.status_code = 404
#          return response

  
# class Verify(Resource):
#   def get(self):
#     token = request.headers['Authorization'].split(" ")[1]
#     print("token-verify-->", token)
#     return validate_token(token, output=True)




parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNom', type=str, help = 'Debe elegir la Descripción del rol', required = True)
class ModificarRol(Resource):
  def post(self):
      data = parseModificarRol.parse_args()
      return modificarRol(data)
  
parseEliminarRol = reqparse.RequestParser()
parseEliminarRol.add_argument('rolId', type=str, help = 'Debe elegir el Id del rol', required = True)
class EliminarRol(Resource):
  def post(self):
      data = parseEliminarRol.parse_args()
      return eliminarRol(data)




# Authentication

from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from functools import wraps
import jwt
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123123123'  # Reemplaza con tu clave secreta
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow())


def encode_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, seconds=30),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('utf-8')


class RegisterUser(Resource):
    def post(self):
        parse_register = reqparse.RequestParser()
        parse_register.add_argument('email', type=str, help='Debe proporcionar un correo electrónico', required=True)
        parse_register.add_argument('password', type=str, help='Debe proporcionar una contraseña', required=True)

        user_data = parse_register.parse_args()
        user = User.query.filter_by(email=user_data['email']).first()

        if not user:
            try:
                hashed_password = generate_password_hash(user_data['password'])
                new_user = User(email=user_data['email'], password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                resp = {
                    "status": "success",
                    "message": "Usuario registrado exitosamente",
                }
                return make_response(jsonify(resp)), 201

            except Exception as e:
                print(e)
                resp = {
                    "status": "error",
                    "message": "Se produjo un error, falló el registro del usuario"
                }
                return make_response(jsonify(resp)), 401
        else:
            resp = {
                "status": "error",
                "message": "El usuario ya existe"
            }
            return make_response(jsonify(resp)), 202



class UserLogin(Resource):
    def post(self):
        parse_login = reqparse.RequestParser()
        parse_login.add_argument('email', type=str, help='Debe proporcionar un correo electrónico', required=True)
        parse_login.add_argument('password', type=str, help='Debe proporcionar una contraseña', required=True)
        
        user_data = parse_login.parse_args()

        try:
            user = User.query.filter_by(email=user_data['email']).first()

            if user and check_password_hash(user.password, user_data['password']):
                auth_token = encode_token(user.id)
                resp = {
                    "status": "success",
                    "message": "Inicio de sesión exitoso",
                    'auth_token': auth_token
                }
                return make_response(jsonify(resp), 200)
            else:
                resp = {
                    "status": "error",
                    "message": "El usuario no existe o la contraseña es incorrecta"
                }
                return make_response(jsonify(resp), 404)

        except Exception as e:
            print(e)
            resp = {
                "status": "error",
                "message": "Error en el inicio de sesión"
            }
            return make_response(jsonify(resp), 404)




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            print(token)
        if not token:
            return {
                       "message": "Authentication Token is missing",
                       "error": "Unauthorized"
                   }, 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.get(data["sub"])
            if current_user is None:
                return {
                           "message": "Invalid Authentication token",
                           "error": "Unauthorized"
                       }, 401
        except Exception as e:
            return {
                       "message": "An error occurred",
                       "error": str(e)
                   }, 500

        return f(current_user, *args, **kwargs)

    return decorated


class ProtectedResource(Resource):
    @token_required
    def get(self, current_user):
        resp = {"message": "This is a protected view", "user_email": current_user.email}
        return make_response(jsonify(resp)), 200


# api.add_resource(RegisterUser, '/register2')
# api.add_resource(UserLogin, '/login2')
# api.add_resource(ProtectedResource, '/protected2')


# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)

