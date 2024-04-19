from flask_restful import Api
import resources.Materia as Materia
from client.routes import Routes as routes

def materia_routes(api: Api):
    api.add_resource(Materia.ListarMateria, routes.listarMateria)
    api.add_resource(Materia.EliminarMateria, routes.eliminarMateria)
    api.add_resource(Materia.InsertarMateria, routes.insertarMateria)
    api.add_resource(Materia.ModificarMateria, routes.modificarMateria)
    api.add_resource(Materia.ListaMateriaCombo, routes.listaMateriaCombo)
    api.add_resource(Materia.GestionarMateriaEstado, routes.gestionarMateriaEstado)