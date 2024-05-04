from flask_restful import Resource, reqparse
from core.auth import *
from services.usuario_service import * # Servicio de usuario
from flask import request

# from resources.Autenticacion import token_required

# @app.route('/register', methods=['POST'])
# parseLogin = reqparse.RequestParser()
# parseLogin.add_argument('email', type=str, help = 'Debe elegir el email', required = True)
# parseLogin.add_argument('password', type=str, help = 'Debe elegir la password', required = True)
# class Login(Resource):
#   print("login -->", parseLogin)
#   def post(self):
#       data = parseLogin.parse_args()
#       return login(data)

# def verify_token_middleware(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         token = request.headers['Authorization'].split(" ")[1]
#         print("token-verify-middleware-->", token)
#         return validate_token(token, output=False)
#     return wrapper

class ListaUsuario(Resource):
  def get(self):
    return listaUsuario()
  
class TipoPersona(Resource):
  def get(self):
    return tipoPersona()

class ListarRoles(Resource):
  def get(self):
      return listarRoles()

parseGestionarUsuario = reqparse.RequestParser()
parseGestionarUsuario.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseGestionarUsuario.add_argument('usuid', type=int, help='Debe elegir usuId')
parseGestionarUsuario.add_argument('perid', type=int, help='Debe elegir perId', required=True)
parseGestionarUsuario.add_argument('rolid', type=int, help='Debe elegir rolId', required=True)
parseGestionarUsuario.add_argument('usuname', type=str, help='Debe elegir usuName', required=True)
parseGestionarUsuario.add_argument('usupassword', type=str, help='Debe elegir usuPassword', required=True)
parseGestionarUsuario.add_argument('usupasswordhash', type=str, help='Debe elegir usuPasswordHash', required=True)
parseGestionarUsuario.add_argument('usuemail', type=str, help='Debe elegir usuEmail', required=True)
parseGestionarUsuario.add_argument('usuimagen', type=str, help='Debe elegir usuImagen', required=True)
parseGestionarUsuario.add_argument('usudescripcion', type=str, help='Debe elegir usuDescripcion', required=True)
parseGestionarUsuario.add_argument('usuestado', type=int, help='Debe elegir estado', required=True)
parseGestionarUsuario.add_argument('usuusureg', type=str, help='Debe elegir usuRe', required=True)
class GestionarUsuario(Resource):
  def post(self):
    data = parseGestionarUsuario.parse_args()
    return gestionarUsuario(data)
  
parseGestionarUsuarioEstado = reqparse.RequestParser()
parseGestionarUsuarioEstado.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseGestionarUsuarioEstado.add_argument('usuid', type=int, help='Debe elegir usuid', required=True)
parseGestionarUsuarioEstado.add_argument('usuusumod', type=str, help='Debe elegir usumod', required=True)
class GestionarUsuarioEstado(Resource):
  def post(self):
    data = parseGestionarUsuarioEstado.parse_args()
    return gestionarUsuarioEstado(data)

parseGestionarUsuarioPassword = reqparse.RequestParser()
parseGestionarUsuarioPassword.add_argument('usuid', type=int, help='Debe elegir usuid', required=True)
parseGestionarUsuarioPassword.add_argument('usupassword', type=str, help='Debe elegir usupassword', required=True)
parseGestionarUsuarioPassword.add_argument('usuusumod', type=str, help='Debe elegir usumod', required=True)
class GestionarUsuarioPassword(Resource):
  def post(self):
    data = parseGestionarUsuarioPassword.parse_args()
    return gestionarUsuarioPassword(data)
    
parsePerfil = reqparse.RequestParser()
parsePerfil.add_argument('usuid', type=int, help = 'Debe elegir el usuid', required = True)
class Perfil(Resource):
  # @token_required
  def post(self):
      data = parsePerfil.parse_args()
      return perfil(data)

parseCrearRol = reqparse.RequestParser()
parseCrearRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseCrearRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseCrearRol.add_argument('rolUsuReg', type=str, help = 'Debe elegir el usuario de registro')
class CrearRol(Resource):
  def post(self):
      data = parseCrearRol.parse_args()
      return crearRol(data)
  
parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseModificarRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseModificarRol.add_argument('rolUsuMod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class ModificarRol(Resource):
  def post(self):
      data = parseModificarRol.parse_args()
      return modificarRol(data)
  
parseEliminarRol = reqparse.RequestParser()
parseEliminarRol.add_argument('rolid', type=str, help = 'Debe elegir el Id del rol', required = True)
parseEliminarRol.add_argument('rolusumod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class EliminarRol(Resource):
  def post(self):
      data = parseEliminarRol.parse_args()
      return eliminarRol(data)

parseObtenerEmail = reqparse.RequestParser()
parseObtenerEmail.add_argument('usuname', type=str, help = 'Debe elegir el usuname', required = True)
parseObtenerEmail.add_argument('usuemail', type=str, help = 'Debe elegir el usuemail', required = True)
class ObtenerEmail(Resource):
  # @token_required
  def post(self):
      data = parseObtenerEmail.parse_args()
      return obtenerEmail(data)







