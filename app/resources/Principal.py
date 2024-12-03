from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.principal_service import *

class ListarCantidades(Resource):
    @token_required
    def get(self):
        return listarCantidades()
    
class ListarEstudiantesMateria(Resource):
    @token_required
    def get(self):
        return listarEstudiantesMateria()

class ListarEstudiantesNivel(Resource):
    @token_required
    def get(self):
        return listarEstudiantesNivel()


