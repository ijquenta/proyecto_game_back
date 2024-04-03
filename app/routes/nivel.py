from flask_restful import Api
import resources.Nivel as Nivel
from client.routes import Routes as routes

def nivel_routes(api: Api):
    api.add_resource(Nivel.ListarNivel, routes.listarNivel)
    api.add_resource(Nivel.InsertarNivel, routes.insertarNivel)
    api.add_resource(Nivel.ModificarNivel, routes.modificarNivel)
    api.add_resource(Nivel.EliminarNivel, routes.eliminarNivel)