from flask_restful import Resource, reqparse
from services.matricula_service import *

class ListarMatricula(Resource):
  def get(self):
      print("Listar Inscripcion")
      return listarMatricula()
    
parseInsertarMatricula = reqparse.RequestParser()
parseInsertarMatricula.add_argument('matrgestion', type=int, help = 'Debe elegir matrgestion', required = True)
parseInsertarMatricula.add_argument('matrestadodescripcion', type=str, help = 'Debe elegir matrestadodescripcion', required = True)
parseInsertarMatricula.add_argument('matrfchini', type=str, help = 'Debe elegir matrfchini', required = True)
parseInsertarMatricula.add_argument('matrfchfin', type=str, help = 'Debe elegir matrfchfin', required = True)
parseInsertarMatricula.add_argument('matrcos', type=int, help = 'Debe elegir matrcos', required = True)
parseInsertarMatricula.add_argument('matrusureg', type=str, help = 'Debe elegir matrusureg', required = True)
parseInsertarMatricula.add_argument('matrestado', type=int, help = 'Debe elegir matrestado', required = True)
class InsertarMatricula(Resource):
  def post(self):
    data = parseInsertarMatricula.parse_args()
    return insertarMatricula(data)
  
parseModificarMatricula = reqparse.RequestParser()
parseModificarMatricula.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
parseModificarMatricula.add_argument('matrgestion', type=int, help = 'Debe elegir matrgestion', required = True)
parseModificarMatricula.add_argument('matrestadodescripcion', type=str, help = 'Debe elegir matrestadodescripcion', required = True)
parseModificarMatricula.add_argument('matrfchini', type=str, help = 'Debe elegir matrfchini', required = True)
parseModificarMatricula.add_argument('matrfchfin', type=str, help = 'Debe elegir matrfchfin', required = True)
parseModificarMatricula.add_argument('matrcos', type=int, help = 'Debe elegir matrcos', required = True)
parseModificarMatricula.add_argument('matrusumod', type=str, help = 'Debe elegir matrusureg', required = True)
parseModificarMatricula.add_argument('matrestado', type=int, help = 'Debe elegir matrestado', required = True)
class ModificarMatricula(Resource):
  def post(self):
    data = parseModificarMatricula.parse_args()
    return modificarMatricula(data)
  
parseEliminarMatricula = reqparse.RequestParser()
parseEliminarMatricula.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
class EliminarMatricula(Resource):
  def post(self):
    data = parseEliminarMatricula.parse_args()
    return eliminarMatricula(data)
  
parseModificarNivel = reqparse.RequestParser()
parseModificarNivel.add_argument('curid', type=int, help = 'Debe elegir curid', required = True)
parseModificarNivel.add_argument('curnombre', type=str, help = 'Debe elegir curnombre', required = True)
parseModificarNivel.add_argument('curestado', type=str, help = 'Debe elegir curestado', required = True)
parseModificarNivel.add_argument('curestadodescripcion', type=str, help = 'Debe elegir curestadodescripcion', required = True)
parseModificarNivel.add_argument('curnivel', type=int, help = 'Debe elegir curnivel', required = True)
parseModificarNivel.add_argument('curfchini', type=str, help = 'Debe elegir curfchini', required = True)
parseModificarNivel.add_argument('curfchfin', type=str, help = 'Debe elegir curfchfin', required = True)
parseModificarNivel.add_argument('curusumod', type=str, help = 'Debe elegir curusumod', required = True)
parseModificarNivel.add_argument('curdesnivel', type=str, help = 'Debe elegir curdesnivel', required = True)
parseModificarNivel.add_argument('curdescripcion', type=str, help = 'Debe elegir curdescripcion', required = True)
class ModificarNivel(Resource):
  def post(self):
    data = parseModificarNivel.parse_args()
    return modificarNivel(data)