from flask_restful import Api
import resources.Principal as Principal
from client.routes import Routes as routes

def principal_routes(api: Api):
    api.add_resource(Principal.ListarCantidades, routes.listarCantidades)
    api.add_resource(Principal.ListarEstudiantesMateria, routes.listarEstudiantesMateria)
    api.add_resource(Principal.ListarEstudiantesNivel, routes.listarEstudiantesNivel)
