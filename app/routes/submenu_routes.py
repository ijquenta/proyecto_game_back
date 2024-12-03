from flask_restful import Api
from client.routes import Routes as routes
# import resources.Menu_resource as menu
import resources.SubMenu_resource as submenu
def submenu_routes(api: Api):
    api.add_resource(submenu.GetListSubMenu, routes.getListSubMenu)
    api.add_resource(submenu.CreateSubMenu, routes.createSubMenu)
    api.add_resource(submenu.UpdateSubMenu, routes.updateSubMenu)
    api.add_resource(submenu.DeleteSubMenu, routes.deleteSubMenu)
    api.add_resource(submenu.GetTipoMenu, routes.getTipoMenu)