from flask_restful import Api
import resources.Asistencia as Asistencia
from client.routes import Routes as routes

def asistencia_routes(api: Api):
    api.add_resource(Asistencia.ListarAsistencia, routes.listarAsistencia)