from flask_restful import Api
# import resources.Operacion as operacion
import resources.Acceso_resource as acceso
from client.routes import Routes as routes

def acceso_routes(api: Api):
    api.add_resource(acceso.GetAccesos, routes.getAccesos)
    api.add_resource(acceso.GetSubMenus, routes.getSubMenus)
    api.add_resource(acceso.GetSubMenuType, routes.getSubMenuType)
    api.add_resource(acceso.CreateAccess, routes.createAccess)
    api.add_resource(acceso.UpdateAccess, routes.updateAccess)
    api.add_resource(acceso.DeleteAccess, routes.deleteAccess)
    api.add_resource(acceso.GetIconoNombre, routes.getIconoNombre)