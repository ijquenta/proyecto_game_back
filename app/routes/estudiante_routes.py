from flask_restful import Api
import resources.Estudiante as Estudiante
from client.routes import Routes as routes

def estudiante_routes(api: Api):
    api.add_resource(Estudiante.ListarEstudiante, routes.listarEstudiante)
    api.add_resource(Estudiante.ObtenerMateriasInscritas, routes.obtenerMateriasInscritas)