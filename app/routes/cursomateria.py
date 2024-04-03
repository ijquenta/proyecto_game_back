from flask_restful import Api
import resources.Curso as Curso
from client.routes import Routes as routes

def cursomateria_routes(api: Api):
    api.add_resource(Curso.ListarCursoMateria, routes.listarCursoMateria)
    api.add_resource(Curso.EliminarCursoMateria, routes.eliminarCursoMateria)
    api.add_resource(Curso.InsertarCursoMateria, routes.insertarCursoMateria)
    api.add_resource(Curso.ModificarCursoMateria, routes.modificarCursoMateria)
    api.add_resource(Curso.TipoRol, routes.tipoRol)
    api.add_resource(Curso.ListaCursoCombo, routes.listaCursoCombo)
    api.add_resource(Curso.ListaPersonaDocenteCombo, routes.listaPersonaDocenteCombo)