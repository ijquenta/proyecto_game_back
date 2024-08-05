from flask_restful import Api
import resources.Materia_resource as Materia_resource
from client.routes import Routes as routes

def materia_routes(api: Api):
    api.add_resource(Materia_resource.ListarMateria, routes.listarMateria)
    api.add_resource(Materia_resource.EliminarMateria, routes.eliminarMateria)
    api.add_resource(Materia_resource.InsertarMateria, routes.insertarMateria)
    api.add_resource(Materia_resource.ModificarMateria, routes.modificarMateria)
    api.add_resource(Materia_resource.ListaMateriaCombo, routes.listaMateriaCombo)
    api.add_resource(Materia_resource.ListaMateriaCombo2, routes.listaMateriaCombo2)
    api.add_resource(Materia_resource.GestionarMateriaEstado, routes.gestionarMateriaEstado)
    api.add_resource(Materia_resource.GetMateriaByIdResource, routes.getMateriaById)