from flask_restful import Api
import resources.Rol as Rol
from client.routes import Routes as routes

def rol_routes(api: Api):
    api.add_resource(Rol.GetRolesResource, routes.getRoles)
    api.add_resource(Rol.ManageRoleResource, routes.manageRole)
    api.add_resource(Rol.ManageRoleStatusResource, routes.manageRoleStatus)
    api.add_resource(Rol.DeleteRoleResource, routes.deleteRole)