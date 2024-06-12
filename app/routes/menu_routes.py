from flask_restful import Api
from client.routes import Routes as routes
import resources.Menu_resource as menu

def menu_routes(api: Api):
    api.add_resource(menu.GetMenus, routes.getMenus)
    api.add_resource(menu.CreateMenu, routes.createMenu)
    api.add_resource(menu.UpdateMenu, routes.updateMenu)
    api.add_resource(menu.DeleteMenu, routes.deleteMenu)
    # api.add_resource(operacion.GetTipoOperacion, routes.getTipoOperacion)
    # api.add_resource(operacion.GetOperations, routes.getOperations)
    # api.add_resource(operacion.CreateOperation, routes.createOperation)
    # api.add_resource(operacion.UpdateOperation, routes.updateOperation)
    # api.add_resource(operacion.DeleteOperation, routes.deleteOperation)