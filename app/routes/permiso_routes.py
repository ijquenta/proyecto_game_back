from flask_restful import Api
import resources.Permiso as permiso
from client.routes import Routes as routes

def permiso_routes(api: Api):
    api.add_resource(permiso.ListarPermiso, routes.listarPermiso)
    api.add_resource(permiso.ListarPermisoRol, routes.listarPermisoRol)
    api.add_resource(permiso.GetPermisos, routes.getPermisos)
    api.add_resource(permiso.GetOperaciones, routes.getOperaciones)
    api.add_resource(permiso.GetRoles, routes.getRoles)
    api.add_resource(permiso.UpdatePermiso, routes.updatePermiso)
    api.add_resource(permiso.AddPermiso, routes.addPermiso)
    api.add_resource(permiso.DeletePermiso, routes.deletePermiso)