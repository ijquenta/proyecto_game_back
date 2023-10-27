from flask_restful import Resource, reqparse
from services.curso_service import *



class ListarCursoMateria(Resource):
  def get(self):
      print("Listar Cursos")
      return listarCursoMateria()
    
class ListaCursoCombo(Resource):
  def get(self):
      print("Lista Curso Combo")
      return listaCursoCombo()
       
parseListaPersonaDocenteCombo = reqparse.RequestParser()
parseListaPersonaDocenteCombo.add_argument('rolnombre', type=str, help='Debe ingresar el nombre del rol', required = True)
class ListaPersonaDocenteCombo(Resource):
  def post(self):
    data = parseListaPersonaDocenteCombo.parse_args()
    return listaPersonaDocenteCombo(data)