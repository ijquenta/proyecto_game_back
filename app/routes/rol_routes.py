from flask_restful import Api
import resources.Rol as Rol
from client.routes import Routes as routes

def rol_routes(api: Api):
    api.add_resource(Rol.ListarRoles, routes.listarRoles)
    api.add_resource(Rol.GestionarRol, routes.gestionarRol)
    api.add_resource(Rol.GestionarRolEstado, routes.gestionarRolEstado)