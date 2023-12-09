from flask_restful import Resource, reqparse
from services.materia_service import *

class ListarMateria(Resource):
  def get(self):
      return listarMateria()

class ListarPersona(Resource):
  def get(self):
      return listarPersona()

parseListaMateriaCombo = reqparse.RequestParser()
parseListaMateriaCombo.add_argument('curnivel', type=int, help='Debe ingresar el id nivel', required = True)
class ListaMateriaCombo(Resource):
  def post(self):
    data = parseListaMateriaCombo.parse_args()
    return listaMateriaCombo(data)

parseCrearRol = reqparse.RequestParser()
parseCrearRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseCrearRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseCrearRol.add_argument('rolUsuReg', type=str, help = 'Debe elegir el usuario de registro')
class CrearRol(Resource):
  def post(self):
      data = parseCrearRol.parse_args()
      return crearRol(data)
  
parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseModificarRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseModificarRol.add_argument('rolUsuMod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class ModificarRol(Resource):
  def post(self):
      data = parseModificarRol.parse_args()
      return modificarRol(data)
  
parseEliminarRol = reqparse.RequestParser()
parseEliminarRol.add_argument('rolid', type=str, help = 'Debe elegir el Id del rol', required = True)
parseEliminarRol.add_argument('rolusumod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class EliminarRol(Resource):
  def post(self):
      data = parseEliminarRol.parse_args()
      return eliminarRol(data)

parseEliminarMateria = reqparse.RequestParser()
parseEliminarMateria.add_argument('matid', type=int, help = 'Debe elegir matid', required = True)
class EliminarMateria(Resource):
  def post(self):
    data = parseEliminarMateria.parse_args()
    return eliminarMateria(data)
  
parseInsertarMateria = reqparse.RequestParser()
parseInsertarMateria.add_argument('matnombre', type=str, help='Debe elegir matnombre', required=True)
parseInsertarMateria.add_argument('matdescripcion', type=str, help='Debe elegir matdescripcion', required=True)
parseInsertarMateria.add_argument('matnivel', type=int, help='Debe elegir matnivel', required=True)
parseInsertarMateria.add_argument('matdesnivel', type=str, help='Debe elegir matdesnivel', required=True)
parseInsertarMateria.add_argument('matestado', type=int, help='Debe elegir matestado', required=True)
parseInsertarMateria.add_argument('matestadodescripcion', type=str, help='Debe elegir matestadodescripcion', required=True)
parseInsertarMateria.add_argument('matusureg', type=str, help='Debe elegir matusureg', required=True)
class InsertarMateria(Resource):
    def post(self):
        data = parseInsertarMateria.parse_args()
        return insertarMateria(data)
      
parseModificarMateria = reqparse.RequestParser()
parseModificarMateria.add_argument('matid', type=int, help='Debe elegir matid', required=True)
parseModificarMateria.add_argument('matnombre', type=str, help='Debe elegir matnombre', required=True)
parseModificarMateria.add_argument('matdescripcion', type=str, help='Debe elegir matdescripcion', required=True)
parseModificarMateria.add_argument('matnivel', type=int, help='Debe elegir matnivel', required=True)
parseModificarMateria.add_argument('matdesnivel', type=str, help='Debe elegir matdesnivel', required=True)
parseModificarMateria.add_argument('matestado', type=int, help='Debe elegir matestado', required=True)
parseModificarMateria.add_argument('matestadodescripcion', type=str, help='Debe elegir matestadodescripcion', required=True)
parseModificarMateria.add_argument('matusumod', type=str, help='Debe elegir matusumod', required=True)
class ModificarMateria(Resource):
    def post(self):
        data = parseModificarMateria.parse_args()
        return modificarMateria(data)