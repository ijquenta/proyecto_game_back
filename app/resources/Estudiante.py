from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
# from core.auth import require_token
from http import HTTPStatus
from services.beneficio_service import *
from services.estudiante_service import *
#import services.beneficio_service as beneficio

# from resources.Autenticacion import token_required

class ListarEstudiante(Resource):
    # method_decorators = [token_required]  # Aplica el decorador a todos los métodos de la clase
    # @token_required
    def get(self):
        return listarEstudiante()
        # return make_response(jsonify(listarUsuarios())), 200
      
parseRegistrarPersona = reqparse.RequestParser()
parseRegistrarPersona.add_argument('pernombres', type=str, help='Nombres de la persona', required=True)
parseRegistrarPersona.add_argument('perapepat', type=str, help='Apellido paterno de la persona', required=True)
parseRegistrarPersona.add_argument('perapemat', type=str, help='Apellido materno de la persona', required=True)
parseRegistrarPersona.add_argument('pertipodoc', type=int, help='Tipo de documento de la persona', required=True)
parseRegistrarPersona.add_argument('pernrodoc', type=int, help='Número de documento de la persona', required=True)
parseRegistrarPersona.add_argument('perusureg', type=str, help='Usuario que registró la persona', required=True)
class RegistrarPersona(Resource):
    # @token_required
    def post(self):
        data = parseRegistrarPersona.parse_args()
        return registrarPersona(data)

parseObtenerMateriasInscritas = reqparse.RequestParser()
parseObtenerMateriasInscritas.add_argument('perid', type=int, help='Ingresar perid', required=True)
class ObtenerMateriasInscritas(Resource):
    # @token_required
    def post(self):
        data = parseObtenerMateriasInscritas.parse_args()
        return obtenerMateriasInscritas(data)

parsePersona = reqparse.RequestParser()
parsePersona.add_argument('tipo', type=int, help='Tipo de operación (1: Crear, 2: Modificar, 3: Eliminar)', required=True)
parsePersona.add_argument('perid', type=int, help='ID de la persona', required=True)
parsePersona.add_argument('pernombres', type=str, help='Nombres de la persona', required=True)
parsePersona.add_argument('perapepat', type=str, help='Apellido paterno de la persona', required=True)
parsePersona.add_argument('perapemat', type=str, help='Apellido materno de la persona', required=True)
parsePersona.add_argument('pertipodoc', type=int, help='Tipo de documento de la persona', required=True)
parsePersona.add_argument('pernrodoc', type=str, help='Número de documento de la persona', required=True)
parsePersona.add_argument('perfecnac', type=str, help='Fecha de nacimiento de la persona')
parsePersona.add_argument('perdirec', type=str, help='Dirección de la persona', required=True)
parsePersona.add_argument('peremail', type=str, help='Correo electrónico de la persona', required=True)
parsePersona.add_argument('percelular', type=str, help='Número de celular de la persona', required=True)
parsePersona.add_argument('pertelefono', type=str, help='Número de teléfono de la persona', required=True)
parsePersona.add_argument('perpais', type=int, help='ID del país de la persona', required=True)
parsePersona.add_argument('perciudad', type=int, help='ID de la ciudad de la persona', required=True)
parsePersona.add_argument('pergenero', type=int, help='ID del género de la persona', required=True)
parsePersona.add_argument('perestcivil', type=int, help='ID del estado civil de la persona', required=True)
parsePersona.add_argument('perfoto', type=str, help='Foto de la persona (como una cadena base64, por ejemplo)', required=True)
parsePersona.add_argument('perestado', type=int, help='Estado de la persona', required=True)
parsePersona.add_argument('perobservacion', type=str, help='Observaciones sobre la persona', required=True)
parsePersona.add_argument('perusureg', type=str, help='Usuario que registró la persona', required=True)
parsePersona.add_argument('perusumod', type=str, help='Usuario que modificó la persona', required=True)
class GestionarPersona(Resource):
    def post(self):
        data = parsePersona.parse_args()
        return gestionarPersona(data)

class TipoDocumento(Resource):
  def get(self):
    return tipoDocumento()
  
class TipoGenero(Resource):
  def get(self):
    return tipoGenero()
  
class TipoPais(Resource):
  def get(self):
    return tipoPais()

class TipoCiudad(Resource):
  def get(self):
    return tipoCiudad()
  
class TipoEstadoCivil(Resource):
  def get(self):
    return tipoEstadoCivil()

parseActualizarDatosPersonales = reqparse.RequestParser()
parseActualizarDatosPersonales.add_argument('perid', type=int, help='ID de la persona - perid', required=True)
parseActualizarDatosPersonales.add_argument('pernrohijos', type=int, help='número de hijos - pernrohijos', required=True)
parseActualizarDatosPersonales.add_argument('perprofesion', type=str, help='Profesión - perprofesion', required=True)
parseActualizarDatosPersonales.add_argument('perfeclugconversion', type=str, help='Fecha, lugar de conversion - perfeclugconversion', required=True)
parseActualizarDatosPersonales.add_argument('perbautismoaguas', type=int, help='Bautismo en aguas - perbautismoaguas', required=True)
parseActualizarDatosPersonales.add_argument('perbautismoespiritu', type=int, help='Bautismo en espiritu - perbautismoespiritu', required=True)
parseActualizarDatosPersonales.add_argument('pernomdiriglesia', type=str, help='Nombre y dirección de la iglesia - pernomdiriglesia', required=True)
parseActualizarDatosPersonales.add_argument('pernompastor', type=str, help='Nombre del pastor - pernompastor', required=True)
parseActualizarDatosPersonales.add_argument('perusumod', type=str, help='Usuario que modificó la persona - perusumod', required=True)
class ActualizarDatosPersonales(Resource):
    def post(self):
        data = parseActualizarDatosPersonales.parse_args()
        return actualizarDatosPersonales(data)  