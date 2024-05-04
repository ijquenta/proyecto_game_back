from flask_restful import Api
import resources.Docente as Docente
from client.routes import Routes as routes

def docente_routes(api: Api):
    api.add_resource(Docente.ListarDocente, routes.listarDocente)
    api.add_resource(Docente.ObtenerMateriasAsignadas, routes.obtenerMateriasAsignadas)
    api.add_resource(Docente.ListarMateriaEstudianteCurso, routes.listarMateriaEstudianteCurso)