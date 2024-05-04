from flask_restful import Resource, reqparse
from services.principal_service import *

class ListarCantidades(Resource):
    def get(self):
        return listarCantidades()
    
class ListarEstudiantesMateria(Resource):
    def get(self):
        return listarEstudiantesMateria()

class ListarEstudiantesNivel(Resource):
    def get(self):
        return listarEstudiantesNivel()


