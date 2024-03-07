from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
# from core.auth import require_token
from http import HTTPStatus
from services.beneficio_service import *
from services.pago_service import *
#import services.beneficio_service as beneficio

from resources.Autenticacion import token_required

class ListarPago(Resource):
    # method_decorators = [token_required]  # Aplica el decorador a todos los métodos de la clase
    # @token_required
    def get(self):
        return listarPago()
        # return make_response(jsonify(listarUsuarios())), 200
      
parsePagoEstudiante = reqparse.RequestParser()
parsePagoEstudiante.add_argument('perid', type=int, help='Ingrese perid', required=True)
class ListarPagoEstudiante(Resource):
    # @token_required
    def post(self):
        data = parsePagoEstudiante.parse_args()
        return listarPagoEstudiante(data)

parsePagoEstudianteMateria = reqparse.RequestParser()
parsePagoEstudianteMateria.add_argument('perid', type=int, help='Ingrese perid', required=True)
parsePagoEstudianteMateria.add_argument('curid', type=int, help='Ingrese curid', required=True)
parsePagoEstudianteMateria.add_argument('matid', type=int, help='Ingrese matid', required=True)
class ListarPagoEstudianteMateria(Resource):
    # @token_required
    def post(self):
        data = parsePagoEstudianteMateria.parse_args()
        return listarPagoEstudianteMateria(data)
      
class ListarPagoCurso(Resource):
    def get(self):
        return listarPagoCurso()  
      
parsePagoEstudiantesMateria = reqparse.RequestParser()
parsePagoEstudiantesMateria.add_argument('curid', type=int, help='Ingrese curid', required=True)
parsePagoEstudiantesMateria.add_argument('matid', type=int, help='Ingrese matid', required=True)
class ListarPagoEstudiantesMateria(Resource):
    # @token_required
    def post(self):
        data = parsePagoEstudiantesMateria.parse_args()
        return listarPagoEstudiantesMateria(data)
      
      
parseGestionarPago = reqparse.RequestParser()
parseGestionarPago.add_argument('tipo', type=int, help='Ingrese tipo', required=True)
parseGestionarPago.add_argument('pagid', type=int, help='Ingrese pagid', required=True)
parseGestionarPago.add_argument('insid', type=int, help='Ingrese insid', required=True)
parseGestionarPago.add_argument('pagdescripcion', type=str, help='Ingrese pagdescripcion', required=True)
parseGestionarPago.add_argument('pagmonto', type=int, help='Ingrese pagmonto', required=True)
parseGestionarPago.add_argument('pagfecha', type=str, help='Ingrese pagfecha', required=True)
parseGestionarPago.add_argument('pagrusureg', type=str, help='Ingrese pagrusureg', required=True)
parseGestionarPago.add_argument('pagestadodescripcion', type=str, help='Ingrese pagestadodescripcion', required=True)
parseGestionarPago.add_argument('pagestado', type=int, help='Ingrese pagestado', required=True)
class GestionarPago(Resource):
    # @token_required
    def post(self):
        data = parseGestionarPago.parse_args()
        return gestionarPago(data)