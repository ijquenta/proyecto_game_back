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
    @token_required
    def post(self):
        data = parsePagoEstudianteMateria.parse_args()
        return listarPagoEstudianteMateria(data)


class ListarPagoCurso(Resource):
    @token_required
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


parseRptPagoEstudianteMateria = reqparse.RequestParser()
parseRptPagoEstudianteMateria.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseRptPagoEstudianteMateria.add_argument('usuname', type=str, help='Ingrese usuname', required=True)
class RptPagoEstudianteMateria(Resource):
    def post(self):
        data = parseRptPagoEstudianteMateria.parse_args()
        return rptPagoEstudianteMateria(data)
    
parseGenerarComprobantePagoEstudiante = reqparse.RequestParser()
parseGenerarComprobantePagoEstudiante.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseGenerarComprobantePagoEstudiante.add_argument('insid', type=int, help='Ingrese insid', required=True)
parseGenerarComprobantePagoEstudiante.add_argument('usuname', type=str, help='Ingrese usuname', required=True)
class GenerarComprobantePagoEstudiante(Resource):
    def post(self):
        data = parseGenerarComprobantePagoEstudiante.parse_args()
        return generarComprobantePagoEstudiante(data)

parseGenerarComprobantePagoMatricula = reqparse.RequestParser()
parseGenerarComprobantePagoMatricula.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseGenerarComprobantePagoMatricula.add_argument('matrid', type=int, help='Ingrese matrid', required=True)
parseGenerarComprobantePagoMatricula.add_argument('usuname', type=str, help='Ingrese usuname', required=True)
class GenerarComprobantePagoMatricula(Resource):
    def post(self):
        data = parseGenerarComprobantePagoMatricula.parse_args()
        return generarComprobantePagoMatricula(data)  
    
    