from flask_restful import Api
import resources.Curso_resource as Curso_resource
from client.routes import Routes as routes

def cursomateria_routes(api: Api):
    api.add_resource(Curso_resource.ListarCursoMateria, routes.listarCursoMateria)
    api.add_resource(Curso_resource.EliminarCursoMateria, routes.eliminarCursoMateria)
    api.add_resource(Curso_resource.InsertarCursoMateria, routes.insertarCursoMateria)
    api.add_resource(Curso_resource.ModificarCursoMateria, routes.modificarCursoMateria)
    api.add_resource(Curso_resource.TipoRol, routes.tipoRol)
    api.add_resource(Curso_resource.ListaCursoCombo, routes.listaCursoCombo)
    api.add_resource(Curso_resource.ListaPersonaDocenteCombo, routes.listaPersonaDocenteCombo)
    api.add_resource(Curso_resource.GestionarCursoMateriaEstado, routes.gestionarCursoMateriaEstado)
    api.add_resource(Curso_resource.GetCursoByIdResource, routes.getCursoById)
    api.add_resource(Curso_resource.GetTipoMateriaByCursoIdResource, routes.getTipoMateriaByCursoId) 
    api.add_resource(Curso_resource.GetTipoCurso, routes.getTipoCurso)
    