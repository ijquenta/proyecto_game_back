from flask_restful import Resource, reqparse
from services.materia_service import *

class ListarMaterias(Resource):
  def get(self):
      print("Listar Materias")
      return listarMaterias()

class ListarPersona(Resource):
  def get(self):
      print("ListarPersona")
      return listarPersona()

class ListarRoles(Resource):
  def get(self):
      print("Rest")
      # return listarRoles()
      
parseListaMateriaCombo = reqparse.RequestParser()
parseListaMateriaCombo.add_argument('curnivel', type=int, help='Debe ingresar el id nivel', required = True)
class ListaMateriaCombo(Resource):
  def post(self):
    data = parseListaMateriaCombo.parse_args()
    # print("ListaMateriaCombo: ", data)
    return listaMateriaCombo(data)

parseCrearRol = reqparse.RequestParser()
parseCrearRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseCrearRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseCrearRol.add_argument('rolUsuReg', type=str, help = 'Debe elegir el usuario de registro')
class CrearRol(Resource):
  def post(self):
      data = parseCrearRol.parse_args()
      # print("CrearRol -->", data)
      return crearRol(data)
  
parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseModificarRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseModificarRol.add_argument('rolUsuMod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class ModificarRol(Resource):
  def post(self):
      data = parseModificarRol.parse_args()
      print("Modificar Rol -->", data)
      return modificarRol(data)
  
parseEliminarRol = reqparse.RequestParser()
parseEliminarRol.add_argument('rolid', type=str, help = 'Debe elegir el Id del rol', required = True)
parseEliminarRol.add_argument('rolusumod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class EliminarRol(Resource):
  def post(self):
      data = parseEliminarRol.parse_args()
      return eliminarRol(data)

