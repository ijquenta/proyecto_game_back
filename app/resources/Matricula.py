from flask_restful import Resource, reqparse
from services.matricula_service import *

class ListarMatricula(Resource):
  def get(self):
      return listarMatricula()
    
parseInsertarMatricula = reqparse.RequestParser()
parseInsertarMatricula.add_argument('matrgestion', type=str, help = 'Debe elegir matrgestion', required = True)
parseInsertarMatricula.add_argument('matrestadodescripcion', type=str, help = 'Debe elegir matrestadodescripcion', required = True)
parseInsertarMatricula.add_argument('matrfchini', type=str, help = 'Debe elegir matrfchini', required = True)
parseInsertarMatricula.add_argument('matrfchfin', type=str, help = 'Debe elegir matrfchfin', required = True)
parseInsertarMatricula.add_argument('matrcos', type=int, help = 'Debe elegir matrcos', required = True)
parseInsertarMatricula.add_argument('matrusureg', type=str, help = 'Debe elegir matrusureg', required = True)
parseInsertarMatricula.add_argument('matrestado', type=int, help = 'Debe elegir matrestado')
class InsertarMatricula(Resource):
  def post(self):
    data = parseInsertarMatricula.parse_args()
    return insertarMatricula(data)
  
parseModificarMatricula = reqparse.RequestParser()
parseModificarMatricula.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
parseModificarMatricula.add_argument('matrgestion', type=str, help = 'Debe elegir matrgestion', required = True)
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

parseGestionarMatriculaEstado = reqparse.RequestParser()
parseGestionarMatriculaEstado.add_argument('tipo', type=int, help = 'Debe elegir tipo', required = True)
parseGestionarMatriculaEstado.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
parseGestionarMatriculaEstado.add_argument('matrusumod', type=str, help = 'Debe elegir matrusmod', required = True)
class GestionarMatriculaEstado(Resource):
  def post(self):
    data = parseGestionarMatriculaEstado.parse_args()
    return gestionarMatriculaEstado(data)