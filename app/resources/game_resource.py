from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from core.auth import *
from services.usuario_service import *

class ListaUsuario(Resource):
  @token_required
  def get(self):
    return listaUsuario()
  
class TipoPersona(Resource):
  @token_required
  def get(self):
    return tipoPersona()
  
class TipoPersonaDocente(Resource):
  @token_required
  def get(self):
    return tipoPersonaDocente()

class ListarRoles(Resource):
  @token_required
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
parseGestionarUsuario.add_argument('usudescripcion', type=str, help='Debe elegir usuDescripcion', required=True)
parseGestionarUsuario.add_argument('usuestado', type=int, help='Debe elegir estado', required=True)
parseGestionarUsuario.add_argument('usuusureg', type=str, help='Debe elegir usuRe', required=True)
class GestionarUsuario(Resource):
  @token_required
  def post(self):
    data = parseGestionarUsuario.parse_args()
    return gestionarUsuario(data)
  
parseGestionarUsuarioEstado = reqparse.RequestParser()
parseGestionarUsuarioEstado.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseGestionarUsuarioEstado.add_argument('usuid', type=int, help='Debe elegir usuid', required=True)
parseGestionarUsuarioEstado.add_argument('usuusumod', type=str, help='Debe elegir usumod', required=True)
class GestionarUsuarioEstado(Resource):
  @token_required
  def post(self):
    data = parseGestionarUsuarioEstado.parse_args()
    return gestionarUsuarioEstado(data)

parseGestionarUsuarioPassword = reqparse.RequestParser()
parseGestionarUsuarioPassword.add_argument('usuid', type=int, help='Debe elegir usuid', required=True)
parseGestionarUsuarioPassword.add_argument('usupassword', type=str, help='Debe elegir usupassword', required=True)
parseGestionarUsuarioPassword.add_argument('usuusumod', type=str, help='Debe elegir usumod', required=True)
class GestionarUsuarioPassword(Resource):
  @token_required
  def post(self):
    data = parseGestionarUsuarioPassword.parse_args()
    return gestionarUsuarioPassword(data)
    
parsePerfil = reqparse.RequestParser()
parsePerfil.add_argument('usuid', type=int, help = 'Debe elegir el usuid', required = True)
class Perfil(Resource):
  @token_required
  def post(self):
      data = parsePerfil.parse_args()
      return perfil(data)

parseCrearRol = reqparse.RequestParser()
parseCrearRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseCrearRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseCrearRol.add_argument('rolUsuReg', type=str, help = 'Debe elegir el usuario de registro')
class CrearRol(Resource):
  @token_required
  def post(self):
      data = parseCrearRol.parse_args()
      return crearRol(data)
  
parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseModificarRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseModificarRol.add_argument('rolUsuMod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class ModificarRol(Resource):
  @token_required
  def post(self):
      data = parseModificarRol.parse_args()
      return modificarRol(data)
  
parseEliminarRol = reqparse.RequestParser()
parseEliminarRol.add_argument('rolid', type=str, help = 'Debe elegir el Id del rol', required = True)
parseEliminarRol.add_argument('rolusumod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class EliminarRol(Resource):
  @token_required
  def post(self):
      data = parseEliminarRol.parse_args()
      return eliminarRol(data)

parseObtenerEmail = reqparse.RequestParser()
parseObtenerEmail.add_argument('usuname', type=str, help = 'Debe elegir el usuname', required = True)
parseObtenerEmail.add_argument('usuemail', type=str, help = 'Debe elegir el usuemail', required = True)
class ObtenerEmail(Resource):
  def post(self):
      data = parseObtenerEmail.parse_args()
      return obtenerEmail(data)
    
    
# change password
# Parser para cambiar la contraseña desde el perfil de usuario
parseChangePassword = reqparse.RequestParser()
parseChangePassword.add_argument('current_password', type=str, required=True, help='Current password cannot be blank')
parseChangePassword.add_argument('new_password', type=str, required=True, help='New password cannot be blank')

# Parser para solicitar el restablecimiento de la contraseña
parseRequestPasswordReset = reqparse.RequestParser()
parseRequestPasswordReset.add_argument('usuemail', type=str, required=True, help='Email cannot be blank')


# Parser para restablecer la contraseña
parseResetPassword = reqparse.RequestParser()
parseResetPassword.add_argument('usuname', type=str, required=True, help='usuname cannot be blank')
parseResetPassword.add_argument('usupassword', type=str, required=True, help='usupassword cannot be blank')
class ResetPasswordResource(Resource):
    def post(self, token):
        data = parseResetPassword.parse_args()
        return resetPassword(token, data)

parseChangePassword = reqparse.RequestParser()
parseChangePassword.add_argument('usuname', type=str, help='Debe elegir el usuname', required=True)
parseChangePassword.add_argument('usuemail', type=str, help='Debe elegir el usuemail', required=True)

class RequestChangePassword(Resource):
    def __init__(self, mail):
        self.usuario_service = UsuarioService(mail)

    def post(self):
        data = parseChangePassword.parse_args()
        return self.usuario_service.request_password_reset(data)  


# Buscar al u suario por su nombre, email de usuario ó el número de documento
parseBuscarUsuario = reqparse.RequestParser()
parseBuscarUsuario.add_argument('usuname', type=str, help='Debe elegir el usuname', required=True)
parseBuscarUsuario.add_argument('usuemail', type=str, help='Debe elegir el usuemail', required=True)
class BuscarUsuario(Resource):
    def post(self):
        data = parseBuscarUsuario.parse_args()
        return buscarUsuario(data)
      
# Resource para restablecer la contraseña
parseChangePassword = reqparse.RequestParser()
parseChangePassword.add_argument('usuname', type=str, required=True, help='usuname cannot be blank')
parseChangePassword.add_argument('usupassword', type=str, required=True, help='usupassword cannot be blank')
class ChangePasswordResource(Resource):
    @token_required
    def post(self):
        data = parseChangePassword.parse_args()
        return changePassword(data)