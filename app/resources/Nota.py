from flask_restful import Resource, reqparse
from services.nota_service import *
from resources.Autenticacion import token_required
import services.nota_service as nota

class ListarNota(Resource):
    def get(self):
        return listarNota()
      
parseNotaEstudiante = reqparse.RequestParser()
parseNotaEstudiante.add_argument('perid', type=int, help='Ingrese perid', required=True)
class ListarNotaEstudiante(Resource):
    # @token_required
    def post(self):
        data = parseNotaEstudiante.parse_args()
        return listarNotaEstudiante(data)

parseNotaDocente = reqparse.RequestParser()
parseNotaDocente.add_argument('perid', type=int, help='Ingrese perid', required=True)
class ListarNotaDocente(Resource):
    def post(self):
        data = parseNotaDocente.parse_args()
        return listarNotaDocente(data)  
    
parseNotaEstudianteMateria = reqparse.RequestParser()
parseNotaEstudianteMateria.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseNotaEstudianteMateria.add_argument('curid', type=int, help='Ingrese curid', required=True)
parseNotaEstudianteMateria.add_argument('matid', type=int, help='Ingrese matid', required=True)
class ListarNotaEstudianteMateria(Resource):
    # @token_required
    def post(self):
        data = parseNotaEstudianteMateria.parse_args()
        return listarNotaEstudianteMateria(data)

parseNotaEstudianteCurso = reqparse.RequestParser()
parseNotaEstudianteCurso.add_argument('curmatid', type=int, help='Ingrese curmatid', required=True)
class ListarNotaEstudianteCurso(Resource):
    def post(self):
        data = parseNotaEstudianteCurso.parse_args()
        return listarNotaEstudianteCurso(data)
    
    
parseRptNotaEstudianteMateria = reqparse.RequestParser()
parseRptNotaEstudianteMateria.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseRptNotaEstudianteMateria.add_argument('usuname', type=str, help='Ingrese usuname', required=True)
class RptNotaEstudianteMateria(Resource):
    def post(self):
        data = parseRptNotaEstudianteMateria.parse_args()
        return nota.rptNotaEstudianteMateria(data)