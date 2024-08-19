from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.materia_service import * # Servicio de materia

class ListarMateria(Resource):
  def get(self):
      return listarMateria()

    
class GetListMateriaCombo(Resource):
  def get(self):
      return getListMateriaCombo()

parseListaMateriaCombo = reqparse.RequestParser()
parseListaMateriaCombo.add_argument('curnivel', type=int, help='Debe ingresar el id nivel', required = True)
class ListaMateriaCombo(Resource):
  def post(self):
    data = parseListaMateriaCombo.parse_args()
    return listaMateriaCombo(data)

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
      
      
parseGestionarMateriaEstado = reqparse.RequestParser()
parseGestionarMateriaEstado.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseGestionarMateriaEstado.add_argument('matid', type=int, help='Debe elegir matid', required=True)
parseGestionarMateriaEstado.add_argument('matusumod', type=str, help='Debe elegir matusumod', required=True)
class GestionarMateriaEstado(Resource):
    def post(self):
        data = parseGestionarMateriaEstado.parse_args()
        return gestionarMateriaEstado(data)
      
class GetMateriaByIdResource(Resource):
    @token_required
    def get(self, matid):
        return getMateriaById(matid)