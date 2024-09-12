from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.acceso_service import * # Servicio de acceso

class GetAccesos(Resource):
    @token_required
    def get(self):
        return list_all_accesses()
    
class GetIconoNombre(Resource):
    @token_required
    def get(self, submenid):
        return getIconoNombre(submenid)

class GetSubMenus(Resource):
    @token_required
    def get(self):
        return getSubMenus()
    
class GetSubMenuType(Resource):
    @token_required
    def get(self):
        return getSubMenuType()
    
parseCreateAccess = reqparse.RequestParser()
parseCreateAccess.add_argument('rolid', type=int, help='Ingrese rolid', required=True)
parseCreateAccess.add_argument('submenid', type=int, help='Ingrese submenuid', required=True)
parseCreateAccess.add_argument('accactivo', type=int, help='Ingrese accactivo', required=True)
parseCreateAccess.add_argument('accusureg', type=str, help='Ingrese accusureg', required=True)
parseCreateAccess.add_argument('accdescripcion', type=str, help='Ingrese accdescripcion', required=False)
parseCreateAccess.add_argument('accestado', type=int, help='Ingrese accestado', required=True)
class CreateAccess(Resource):
    @token_required
    def post(self):
        data = parseCreateAccess.parse_args()
        return createAccess(data)
    
parseUpdateAccess = reqparse.RequestParser()
parseUpdateAccess.add_argument('accactivo', type=int, help='Ingrese accactivo', required=True)
parseUpdateAccess.add_argument('accusumod', type=str, help='Ingrese accusumod', required=True)  
class UpdateAccess(Resource):
    @token_required
    def put(self, accid):
        data = parseUpdateAccess.parse_args()
        return updateAccess(data, accid)
    
parseDeleteAccess = reqparse.RequestParser()
class DeleteAccess(Resource):
    @token_required
    def delete(self, accid):
        return deleteAccess(accid)
    
