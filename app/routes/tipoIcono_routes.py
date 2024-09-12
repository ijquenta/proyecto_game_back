from flask_restful import Api
from client.routes import Routes as routes
# import resources.Menu_resource as menu
import resources.TipoIcono_resource as tipoIcono

def tipoIcono_routes(api: Api):
    api.add_resource(tipoIcono.GetTipoIcono, routes.getTipoIcono)
    api.add_resource(tipoIcono.FindIdIcono, routes.findIdIcono)