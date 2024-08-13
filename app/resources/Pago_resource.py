from flask import request
from flask_restful import Resource, reqparse
# Servicio de pago
from services.pago_service import *  
# Token required
from resources.Autenticacion import token_required

# Payment
# Obtener todos los pagos
class GetPayments(Resource):
    @token_required    
    def get(self):
        return getPayments()

class ListarPago(Resource):
    @token_required
    def get(self):
        return getAllPayments()
    

parsePagoEstudiante = reqparse.RequestParser()
parsePagoEstudiante.add_argument('perid', type=int, help='Ingrese perid', required=True)
# Obtener los pago de un estudiante
class ListarPagoEstudiante(Resource):
    @token_required
    def post(self):
        data = parsePagoEstudiante.parse_args()
        # return listarPagoEstudiante(data)
        return getAllPaymentsForOneStudent(data)


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
        # return listarPagoCurso()
        return getAllPaymentsCourse()                                               


class GetPagoByIdResource(Resource):
    @token_required
    def get(self, pagid):
        return getPagoById(pagid)
    
parsePagoEstudiantesMateria = reqparse.RequestParser()
parsePagoEstudiantesMateria.add_argument('curid', type=int, help='Ingrese curid', required=True)
parsePagoEstudiantesMateria.add_argument('matid', type=int, help='Ingrese matid', required=True)
class ListarPagoEstudiantesMateria(Resource):
    @token_required
    def post(self):
        data = parsePagoEstudiantesMateria.parse_args()
        # return listarPagoEstudiantesMateria(data)
        return getPagoEstudianteMateria(data)


parseManagePayment = reqparse.RequestParser()
parseManagePayment.add_argument('tipo', type=int, help='Ingrese tipo', required=True)
parseManagePayment.add_argument('pagid', type=int, help='Ingrese pagid')
parseManagePayment.add_argument('insid', type=int, help='Ingrese insid')
parseManagePayment.add_argument('pagdescripcion', type=str, help='Ingrese pagdescripcion')
parseManagePayment.add_argument('pagmonto', type=float, help='Ingrese pagmonto', required=True)
parseManagePayment.add_argument('pagfecha', type=str, help='Ingrese pagfecha', required=True)
parseManagePayment.add_argument('pagusureg', type=str, help='Ingrese pagusureg')
parseManagePayment.add_argument('pagusumod', type=str, help='Ingrese pagusureg')
parseManagePayment.add_argument('pagestado', type=int, help='Ingrese pagestado')
parseManagePayment.add_argument('pagtipo', type=int, help='Ingrese pagtipo' )
class ManagePayment(Resource):
    @token_required
    def post(self):
        data = parseManagePayment.parse_args()
        return managePayment(data, request)               

parseManageAssignPayment = reqparse.RequestParser()
parseManageAssignPayment.add_argument('tipo', type=int, help='Ingrese tipo', required=True)
parseManageAssignPayment.add_argument('pagid', type=int, help='Ingrese pagid')
parseManageAssignPayment.add_argument('matrid', type=int, help='Ingrese matrid')
parseManageAssignPayment.add_argument('pagdescripcion', type=str, help='Ingrese pagdescripcion')
parseManageAssignPayment.add_argument('pagmonto', type=float, help='Ingrese pagmonto', required=True)
parseManageAssignPayment.add_argument('pagfecha', type=str, help='Ingrese pagfecha', required=True)
parseManageAssignPayment.add_argument('pagusureg', type=str, help='Ingrese pagusureg')
parseManageAssignPayment.add_argument('pagusumod', type=str, help='Ingrese pagusureg')
parseManageAssignPayment.add_argument('pagestado', type=int, help='Ingrese pagestado')
parseManageAssignPayment.add_argument('pagtipo', type=int, help='Ingrese pagtipo' )
class ManageAssignPayment(Resource):
    @token_required
    def post(self):
        data = parseManageAssignPayment.parse_args()
        return manageAssignPayment(data, request)
    
class TipoPago(Resource):
    def get(self):
        return tipoPago()



# Resource secundarios
"""
# Insertar Pago
parseInsertarPago = reqparse.RequestParser()
parseInsertarPago.add_argument(
    'pagdescripcion', type=str, help='Ingrese pagdescripcion', required=True)
parseInsertarPago.add_argument(
    'pagmonto', type=float, help='Ingrese pagmonto', required=True)
parseInsertarPago.add_argument(
    'pagarchivo', type=str, help='Ingrese pagarchivo')
parseInsertarPago.add_argument(
    'pagfecha', type=str, help='Ingrese pagfecha', required=True)
parseInsertarPago.add_argument(
    'pagusureg', type=str, help='Ingrese pagusureg', required=True)
parseInsertarPago.add_argument(
    'pagtipo', type=int, help='Ingrese pagtipo', required=True)


class InsertarPago(Resource):
    # @token_required
    def post(self):
        data = parseInsertarPago.parse_args()
        return insertarPago(data)


parseModificarPago = reqparse.RequestParser()
parseModificarPago.add_argument(
    'pagid', type=int, help='Ingrese pagid', required=True)
parseModificarPago.add_argument(
    'pagdescripcion', type=str, help='Ingrese pagdescripcion', required=True)
parseModificarPago.add_argument(
    'pagmonto', type=float, help='Ingrese pagmonto', required=True)
parseModificarPago.add_argument(
    'pagarchivo', type=str, help='Ingrese pagarchivo')
parseModificarPago.add_argument(
    'pagfecha', type=str, help='Ingrese pagfecha', required=True)
parseModificarPago.add_argument(
    'pagusumod', type=str, help='Ingrese pagusureg', required=True)
parseModificarPago.add_argument(
    'pagtipo', type=int, help='Ingrese pagtipo', required=True)
parseModificarPago.add_argument(
    'archivobol', type=int, help='Ingrese archivobol', required=True)


class ModificarPago(Resource):
    # @token_required
    def post(self):
        data = parseModificarPago.parse_args()
        return modificarPago(data)


# Asignar Pago a Inscripcion
parseAsignarPagoInscripcion = reqparse.RequestParser()
parseAsignarPagoInscripcion.add_argument(
    'insid', type=int, help='Ingrese insid', required=True)
parseAsignarPagoInscripcion.add_argument(
    'pagid', type=int, help='Ingrese pagid', required=True)
parseAsignarPagoInscripcion.add_argument(
    'pagusumod', type=str, help='Ingrese pagusureg', required=True)


class AsignarPagoInscripcion(Resource):
    # @token_required
    def post(self):
        data = parseAsignarPagoInscripcion.parse_args()
        return asignarPagoInscripcion(data)


# Asignar pago a matricula
parseAsignarPagoMatricula = reqparse.RequestParser()
parseAsignarPagoMatricula.add_argument(
    'matrid', type=int, help='Ingrese matrid', required=True)
parseAsignarPagoMatricula.add_argument(
    'pagid', type=int, help='Ingrese pagid', required=True)
parseAsignarPagoMatricula.add_argument(
    'matrusumod', type=str, help='Ingrese matrusumod', required=True)


class AsignarPagoMatricula(Resource):
    # @token_required
    def post(self):
        data = parseAsignarPagoMatricula.parse_args()
        return asignarPagoMatricula(data)


class ObtenerUltimoPago(Resource):
    def get(self):
        return obtenerUltimoPago()
"""