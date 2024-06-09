from flask_restful import Resource, reqparse
from services.permiso_service import * # Servicio de permiso
from services.operacion_service import *

class GetOperations(Resource):
    def get(self):
        return getOperations()
    

parseCreateOperation = reqparse.RequestParser()
parseCreateOperation.add_argument('openombre', type=str, help='Ingrese openombre', required=True)
parseCreateOperation.add_argument('opeusureg', type=str, help='Ingrese opeusureg', required=True)
parseCreateOperation.add_argument('opedescripcion', type=str, help='Ingrese opedescripcion', required=False)
parseCreateOperation.add_argument('opeestado', type=int, help='Ingrese opeestado', required=True)
class CreateOperation(Resource):
    def post(self):
        data = parseCreateOperation.parse_args()
        return createOperation(data)

parseUpdateOperation = reqparse.RequestParser()   
parseUpdateOperation.add_argument('openombre', type=str, help='Ingrese openombre', required=False)  
parseUpdateOperation.add_argument('opeusumod', type=str, help='Ingrese opeusumod', required=True)
parseUpdateOperation.add_argument('opedescripcion', type=str, help='Ingrese opedescripcion', required=False)
parseUpdateOperation.add_argument('opeestado', type=int, help='Ingrese opestado', required=False)
class UpdateOperation(Resource):
    def put(self, opeid):
        data = parseUpdateOperation.parse_args()
        return updateOperation(data, opeid)
    
class DeleteOperation(Resource):
    def delete(self, opeid):
        return deleteOperation(opeid)


parseCreateAccess = reqparse.RequestParser()
parseCreateAccess.add_argument('rolid', type=int, help='Ingrese rolid', required=True)
parseCreateAccess.add_argument('submenid', type=int, help='Ingrese submenuid', required=True)
parseCreateAccess.add_argument('accactivo', type=int, help='Ingrese accactivo', required=True)
parseCreateAccess.add_argument('accusureg', type=str, help='Ingrese accusureg', required=True)
parseCreateAccess.add_argument('accdescripcion', type=str, help='Ingrese accdescripcion', required=False)
parseCreateAccess.add_argument('accestado', type=int, help='Ingrese accestado', required=True)
class CreateAccess(Resource):
    def post(self):
        data = parseCreateAccess.parse_args()
        return createAccess(data)
    
parseUpdateAccess = reqparse.RequestParser()
parseUpdateAccess.add_argument('accactivo', type=int, help='Ingrese accactivo', required=True)
parseUpdateAccess.add_argument('accusumod', type=str, help='Ingrese accusumod', required=True)  
class UpdateAccess(Resource):
    def put(self, accid):
        data = parseUpdateAccess.parse_args()
        return updateAccess(data, accid)
    
parseDeleteAccess = reqparse.RequestParser()
class DeleteAccess(Resource):
    def delete(self, accid):
        return deleteAccess(accid)

class GetTipoOperacion(Resource):
    def get(self):
        return getTipoOperacion()



