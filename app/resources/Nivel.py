from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.nivel_service import * # Servicio de nivel

class ListarNivel(Resource):
  @token_required
  def get(self):
      return listarNivel()

parseInsertarNivel = reqparse.RequestParser()
parseInsertarNivel.add_argument('curnombre', type=str, help = 'Debe elegir curnombre', required = True)
parseInsertarNivel.add_argument('curestado', type=str, help = 'Debe elegir curnombre', required = True)
parseInsertarNivel.add_argument('curestadodescripcion', type=str, help = 'Debe elegir curestadodescripcion', required = True)
parseInsertarNivel.add_argument('curnivel', type=int, help = 'Debe elegir curnivel', required = True)
parseInsertarNivel.add_argument('curfchini', type=str, help = 'Debe elegir numero curfchini', required = True)
parseInsertarNivel.add_argument('curfchfin', type=str, help = 'Debe elegir curfchfin', required = True)
parseInsertarNivel.add_argument('curusureg', type=str, help = 'Debe elegir curusureg', required = True)
parseInsertarNivel.add_argument('curusumod', type=str, help = 'Debe elegir curusumod', required = True)
parseInsertarNivel.add_argument('curdesnivel', type=str, help = 'Debe elegir curdesnivel', required = True)
parseInsertarNivel.add_argument('curdescripcion', type=str, help = 'Debe elegir curdescripcion', required = True)
class InsertarNivel(Resource):
  @token_required
  def post(self):
    data = parseInsertarNivel.parse_args()
    return insertarNivel(data)
  
parseEliminarNivel = reqparse.RequestParser()
parseEliminarNivel.add_argument('curid', type=int, help = 'Debe elegir curid', required = True)
class EliminarNivel(Resource):
  @token_required
  def post(self):
    data = parseEliminarNivel.parse_args()
    return eliminarNivel(data)
  
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
  @token_required
  def post(self):
    data = parseModificarNivel.parse_args()
    return modificarNivel(data)
  
  
parseGestionarNivelEstado = reqparse.RequestParser()
parseGestionarNivelEstado.add_argument('tipo', type=int, help = 'Debe elegir tipo', required = True)
parseGestionarNivelEstado.add_argument('curid', type=int, help = 'Debe elegir curid', required = True)
parseGestionarNivelEstado.add_argument('curusumod', type=str, help = 'Debe elegir curusumod', required = True)
class GestionarNivelEstado(Resource):
  @token_required
  def post(self):
    data = parseGestionarNivelEstado.parse_args()
    return gestionarNivelEstado(data)