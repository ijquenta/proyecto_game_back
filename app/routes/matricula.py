from flask_restful import Api
import resources.Matricula as Matricula
from client.routes import Routes as routes

def matricula_routes(api: Api):
    api.add_resource(Matricula.ListarMatricula, routes.listarMatricula)
    api.add_resource(Matricula.InsertarMatricula, routes.insertarMatricula)
    api.add_resource(Matricula.ModificarMatricula, routes.modificarMatricula)
    api.add_resource(Matricula.EliminarMatricula, routes.eliminarMatricula)