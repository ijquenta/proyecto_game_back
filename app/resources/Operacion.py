from flask_restful import Resource, reqparse
from services.permiso_service import * # Servicio de permiso
from services.operacion_service import *


class GetTipoOperacion(Resource):
    def get(self):
        return getTipoOperacion()



class ListarPermiso(Resource):
    def get(self):
        return listarPermiso()

class ListarPermisoRol(Resource):
    def get(self):
        return "listarPermisoRol"

class GetPermisos(Resource):
    def get(self):
        return getPermisos()
    
class GetRoles(Resource):
    def get(self):
        return getRoles()
    
class GetOperaciones(Resource):
    def get(self):
        return getOperaciones()
    
parseUpdatePermiso = reqparse.RequestParser()
parseUpdatePermiso.add_argument('permid', type=int, help='Ingrese permid', required=True)
parseUpdatePermiso.add_argument('permactivo', type=int, help='Ingrese permactivo', required=True)
parseUpdatePermiso.add_argument('permusumod', type=str, help='Ingrese permusureg', required=True)
class UpdatePermiso(Resource):
    def post(self):
        data = parseUpdatePermiso.parse_args()
        return updatePermiso(data)

parseAddPermiso = reqparse.RequestParser()
parseAddPermiso.add_argument('rolid', type=int, required=True, help='Ingrese rolid')
parseAddPermiso.add_argument('opeid', type=int, required=True, help='Ingrese opeid')
parseAddPermiso.add_argument('permactivo', type=int, required=True, help='Ingrese permactivo')
parseAddPermiso.add_argument('permusureg', type=str, required=True, help='Ingrese permusureg')
parseAddPermiso.add_argument('permdescripcion', type=str, required=False, help='Ingrese permdescripcion')
parseAddPermiso.add_argument('permestado', type=int, default=1, help='Ingrese permestado')
class AddPermiso(Resource):
    def post(self):
        data = parseAddPermiso.parse_args()
        return addPermiso(data)
