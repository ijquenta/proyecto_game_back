from flask_restful import Resource, reqparse
from services.contabilidad_service import * # Servicio de contabilidad
# from core.auth import require_token
# from resources.Autenticacion import token_required

parseListarCursoMateriaContabilidad = reqparse.RequestParser()
parseListarCursoMateriaContabilidad.add_argument('fecini', type=str, help='Ingrese fecha inicio', required=True)
parseListarCursoMateriaContabilidad.add_argument('fecfin', type=str, help='Ingrese fecha fin', required=True)
class ListarCursoMateriaContabilidad(Resource):
    # @token_required
    def post(self):
        data = parseListarCursoMateriaContabilidad.parse_args()
        return listarCursoMateriaContabilidad(data)
