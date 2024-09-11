from flask_restful import Resource, reqparse
from services.docente_service import * # Servicio de docente
from resources.Autenticacion import token_required

class ListarDocente(Resource):
    # method_decorators = [token_required]  # Aplica el decorador a todos los métodos de la clase
    # @token_required
    def get(self):
        return listarDocente()

parseObtenerMateriasAsignadas = reqparse.RequestParser()
parseObtenerMateriasAsignadas.add_argument('perid', type=int, help='Ingresar perid', required=True)
class ObtenerMateriasAsignadas(Resource):
    @token_required
    def post(self):
        data = parseObtenerMateriasAsignadas.parse_args()
        return obtenerMateriasAsignadas(data)
  
parseMateriaEstudianteCurso = reqparse.RequestParser()
parseMateriaEstudianteCurso.add_argument('curmatid', type=int, help='Ingrese curmatid', required=True)
class ListarMateriaEstudianteCurso(Resource):
    @token_required
    def post(self):
        data = parseMateriaEstudianteCurso.parse_args()
        return listarMateriaEstudianteCurso(data)