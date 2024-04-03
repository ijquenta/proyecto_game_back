from flask_restful import Api
import resources.Material as Material
from client.routes import Routes as routes

def material_routes(api: Api):
    api.add_resource(Material.ListarMaterial, routes.listarMaterial)
    api.add_resource(Material.ListarTexto, routes.listarTexto)
    api.add_resource(Material.InsertarTexto, routes.insertarTexto)