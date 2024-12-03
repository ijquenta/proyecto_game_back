from flask_restful import Api
import resources.Operacion as operacion
from client.routes import Routes as routes

def operacion_routes(api: Api):
    api.add_resource(operacion.GetTipoOperacion, routes.getTipoOperacion)
    api.add_resource(operacion.GetOperations, routes.getOperations)
    api.add_resource(operacion.CreateOperation, routes.createOperation)
    api.add_resource(operacion.UpdateOperation, routes.updateOperation)
    api.add_resource(operacion.DeleteOperation, routes.deleteOperation)