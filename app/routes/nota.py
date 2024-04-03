from flask_restful import Api
import resources.Nota as Nota
from client.routes import Routes as routes

def nota_routes(api: Api):
    api.add_resource(Nota.ListarNota, routes.listarNota)
    api.add_resource(Nota.GestionarNota, routes.gestionarNota)
    api.add_resource(Nota.ListarNotaEstudiante, routes.listarNotaEstudiante)
    api.add_resource(Nota.ListarNotaDocente, routes.listarNotaDocente)
    api.add_resource(Nota.ListarNotaEstudianteMateria, routes.listarNotaEstudianteMateria)
    api.add_resource(Nota.ListarNotaEstudianteCurso, routes.listarNotaEstudianteCurso)
    api.add_resource(Nota.RptNotaEstudianteMateria, routes.rptNotaEstudianteMateria)
    api.add_resource(Nota.ListarNotaCurso, routes.listarNotaCurso)