from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.rol_service import *


parseManageRole = reqparse.RequestParser()
parseManageRole.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseManageRole.add_argument('rolid', type=int, help='Debe elegir rolid', required=True)
parseManageRole.add_argument('rolnombre', type=str, help='Debe elegir rolnombre', required=True)
parseManageRole.add_argument('roldescripcion', type=str, help='Debe elegir roldescripcion', required=True)
parseManageRole.add_argument('rolestado', type=int, help='Debe elegir rolestado', required=True)
parseManageRole.add_argument('rolusureg', type=str, help='Debe elegir rolusureg')
parseManageRole.add_argument('rolusumod', type=str, help='Debe elegir rolusumod')

parseManageRoleStatus = reqparse.RequestParser()
parseManageRoleStatus.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)  
parseManageRoleStatus.add_argument('rolid', type=int, help='Debe elegir rolid', required=True)  
parseManageRoleStatus.add_argument('rolusumod', type=str, help='Debe elegir rolusumod', required=True)

class GetRolesResource(Resource):
  @token_required
  def get(self):
      return getRoles()

class ManageRoleResource(Resource):
  @token_required
  def post(self):
    data = parseManageRole.parse_args()
    return manageRole(data)
  
class ManageRoleStatusResource(Resource):
  @token_required
  def post(self):  
    data = parseManageRoleStatus.parse_args()
    return manageRoleStatus(data)

class DeleteRoleResource(Resource):
  @token_required
  def delete(self, rolid):
      return deleteRole(rolid)

