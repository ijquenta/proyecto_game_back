from flask_restful import Resource, reqparse
from services.asistencia_service import * # Servicio asistencia
# from core.auth import require_token
# from resources.Autenticacion import token_required

class ListarAsistencia(Resource):
    # method_decorators = [token_required]  # Aplica el decorador a todos los métodos de la clase
    # @token_required
    def get(self):
        return listarAsistencia()