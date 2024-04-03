from flask_restful import Api
import resources.Inscripcion as Inscripcion
from client.routes import Routes as routes

def inscripcion_routes(api: Api):
    api.add_resource(Inscripcion.ListarInscripcion, routes.listarInscripcion)
    api.add_resource(Inscripcion.InsertarInscripcion, routes.insertarInscripcion)
    api.add_resource(Inscripcion.ModificarInscripcion, routes.modificarInscripcion)
    api.add_resource(Inscripcion.EliminarInscripcion, routes.eliminarInscripcion)
    api.add_resource(Inscripcion.ObtenerCursoMateria, routes.obtenerCursoMateria)
    api.add_resource(Inscripcion.ListarComboCursoMateria, routes.listarComboCursoMateria)
    api.add_resource(Inscripcion.ListarComboMatricula, routes.listarComboMatricula)