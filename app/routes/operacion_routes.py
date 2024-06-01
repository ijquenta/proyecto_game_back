from flask_restful import Api
import resources.Operacion as operacion
from client.routes import Routes as routes

def operacion_routes(api: Api):
    api.add_resource(operacion.GetTipoOperacion, routes.getTipoOperacion)