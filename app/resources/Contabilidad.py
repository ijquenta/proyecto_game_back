from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.contabilidad_service import * # Servicio de contabilidad

parseListarCursoMateriaContabilidad = reqparse.RequestParser()
parseListarCursoMateriaContabilidad.add_argument('fecini', type=str, help='Ingrese fecha inicio', required=True)
parseListarCursoMateriaContabilidad.add_argument('fecfin', type=str, help='Ingrese fecha fin', required=True)
class ListarCursoMateriaContabilidad(Resource):
    @token_required
    def post(self):
        data = parseListarCursoMateriaContabilidad.parse_args()
        return getListCursoMateriaContabilidad(data)


parseGetListCursoMateriaContabilidadById = reqparse.RequestParser()
parseGetListCursoMateriaContabilidadById.add_argument('curid', type=int, help='Ingrese ID del curso', required=True)
parseGetListCursoMateriaContabilidadById.add_argument('matid', type=int, help='Ingrese ID de la materia', required=True)
class GetListCursoMateriaContabilidadById(Resource):
    @token_required
    def post(self):
        data = parseGetListCursoMateriaContabilidadById.parse_args()
        return getListCursoMateriaContabilidadById(data)