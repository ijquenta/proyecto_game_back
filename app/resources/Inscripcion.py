from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.inscripcion_service import * # Servicio de inscripcion

class ListarInscripcion(Resource):
  @token_required
  def get(self):
      return listarInscripcion()
    
class ListarComboCursoMateria(Resource):
  @token_required
  def get(self):
      return listarComboCursoMateria()
    
class ListarComboMatricula(Resource):
  @token_required
  def get(self):
      return listarComboMatricula()
    
parseListarComboMatriculaEstudiante = reqparse.RequestParser()
parseListarComboMatriculaEstudiante.add_argument('peridestudiante', type=int, help = 'Debe elegir peridestudiante', required = True)
class ListarComboMatriculaEstudiante(Resource):
  @token_required
  def post(self):
    data = parseListarComboMatriculaEstudiante.parse_args()
    return listarComboMatriculaEstudiante(data)

parseInsertarInscripcion = reqparse.RequestParser()
parseInsertarInscripcion.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
parseInsertarInscripcion.add_argument('peridestudiante', type=int, help = 'Debe elegir peridestudiante', required = True)
parseInsertarInscripcion.add_argument('pagid', type=int, help = 'Debe elegir pagid', required = True)
parseInsertarInscripcion.add_argument('insusureg', type=str, help = 'Debe elegir insusureg', required = True)
parseInsertarInscripcion.add_argument('curmatid', type=int, help = 'Debe elegir numero curmatid', required = True)
parseInsertarInscripcion.add_argument('insestado', type=int, help = 'Debe elegir insestado', required = True)
parseInsertarInscripcion.add_argument('insestadodescripcion', type=str, help = 'Debe elegir insestadodescripcion', required = True)
class InsertarInscripcion(Resource):
  @token_required
  def post(self):
    data = parseInsertarInscripcion.parse_args()
    return insertarInscripcion(data)
  
parseModificarInscripcion = reqparse.RequestParser()
parseModificarInscripcion.add_argument('insid', type=int, help = 'Debe elegir insid', required = True)
parseModificarInscripcion.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
parseModificarInscripcion.add_argument('peridestudiante', type=int, help = 'Debe elegir peridestudiante', required = True)
parseModificarInscripcion.add_argument('pagid', type=int, help = 'Debe elegir pagid', required = True)
parseModificarInscripcion.add_argument('insusumod', type=str, help = 'Debe elegir insusureg', required = True)
parseModificarInscripcion.add_argument('curmatid', type=int, help = 'Debe elegir numero curmatid', required = True)
parseModificarInscripcion.add_argument('insestado', type=int, help = 'Debe elegir insestado', required = True)
parseModificarInscripcion.add_argument('insestadodescripcion', type=str, help = 'Debe elegir insestadodescripcion', required = True)
class ModificarInscripcion(Resource):
  @token_required
  def post(self):
    data = parseModificarInscripcion.parse_args()
    return modificarInscripcion(data)
  
parseObtenerCursoMateria = reqparse.RequestParser()
parseObtenerCursoMateria.add_argument('curid', type=int, help = 'Debe elegir curid', required = True)
parseObtenerCursoMateria.add_argument('matid', type=int, help = 'Debe elegir matid', required = True)
class ObtenerCursoMateria(Resource):
  @token_required
  def post(self):
    data = parseObtenerCursoMateria.parse_args()
    return obtenerCursoMateria(data)
  
parseEliminarInscripcion = reqparse.RequestParser()
parseEliminarInscripcion.add_argument('insid', type=int, help = 'Debe elegir insid', required = True)
class EliminarInscripcion(Resource):
  @token_required
  def post(self):
    data = parseEliminarInscripcion.parse_args()
    return eliminarInscripcion(data)
  
  
parseGestionarInscripcionEstado = reqparse.RequestParser()
parseGestionarInscripcionEstado.add_argument('tipo', type=int, help = 'Debe elegir tipo', required = True)
parseGestionarInscripcionEstado.add_argument('insid', type=int, help = 'Debe elegir insid', required = True)
parseGestionarInscripcionEstado.add_argument('insusumod', type=str, help = 'Debe elegir insusumod', required = True)
class GestionarInscripcionEstado(Resource):
  @token_required
  def post(self):
    data = parseGestionarInscripcionEstado.parse_args()
    return gestionarInscripcionEstado(data)
  
parseObtenerEstudiantesInscritos = reqparse.RequestParser()
parseObtenerEstudiantesInscritos.add_argument('curid', type=int, help = 'Debe elegir curid', required = True)
parseObtenerEstudiantesInscritos.add_argument('matid', type=int, help = 'Debe elegir matid', required = True)
parseObtenerEstudiantesInscritos.add_argument('curmatfecini', type=str, help = 'Debe elegir curmatfecini', required = True)
parseObtenerEstudiantesInscritos.add_argument('curmatfecfin', type=str, help = 'Debe elegir curmatfecfin', required = True)
class ObtenerEstudiantesInscritos(Resource):
  @token_required
  def post(self):
    data = parseObtenerEstudiantesInscritos.parse_args()
    return obtenerEstudiantesInscritos(data)
  
class GetCursoMateriaByIds(Resource):
  @token_required
  def post(self):
      data = parseObtenerEstudiantesInscritos.parse_args()
      return getCursoMateriaByIds(data)
  