from flask_restful import Resource, reqparse
from services.asistencia_service import * # Servicio asistencia
from resources.Autenticacion import token_required

class ListarAsistencia(Resource):
    @token_required
    def get(self):
        return listarAsistencia()