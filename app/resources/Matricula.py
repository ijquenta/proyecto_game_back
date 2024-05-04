from flask_restful import Resource, reqparse
from services.matricula_service import * # Servicio de matricula

class ListarMatricula(Resource):
  def get(self):
      return listarMatricula()
    
class ListarTipoMatricula(Resource):
  def get(self):
    return listarTipoMatricula()
  
class ListarTipoMatriculaCombo(Resource):
  def get(self):
    return listarTipoMatriculaCombo()
  
class ListarTipoPersonaEstudiante(Resource):
  def get(self):
    return listarTipoPersonaEstudiante()
  
parseInsertarTipoMatricula = reqparse.RequestParser()
parseInsertarTipoMatricula.add_argument('tipmatrgestion', type=str, help = 'Debe elegir tipmatrgestion', required = True)
parseInsertarTipoMatricula.add_argument('tipmatrfecini', type=str, help = 'Debe elegir tipmatrfecini', required = True)
parseInsertarTipoMatricula.add_argument('tipmatrfecfin', type=str, help = 'Debe elegir tipmatrfecini', required = True)
parseInsertarTipoMatricula.add_argument('tipmatrcosto', type=int, help = 'Debe elegir tipmatrcosto', required = True) 
parseInsertarTipoMatricula.add_argument('tipmatrusureg', type=str, help = 'Debe elegir tipmatrusureg', required = True)
parseInsertarTipoMatricula.add_argument('tipmatrdescripcion', type=str, help = 'Debe elegir tipmatrdescripcion')
class InsertarTipoMatricula(Resource):
  def post(self): 
    data = parseInsertarTipoMatricula.parse_args()
    return insertarTipoMatricula(data)
  
parseModificarTipoMatricula = reqparse.RequestParser()
parseModificarTipoMatricula.add_argument('tipmatrid', type=int, help = 'Debe elegir tipmatrid', required = True)
parseModificarTipoMatricula.add_argument('tipmatrgestion', type=str, help = 'Debe elegir tipmatrgestion', required = True)
parseModificarTipoMatricula.add_argument('tipmatrfecini', type=str, help = 'Debe elegir tipmatrfecini', required = True)
parseModificarTipoMatricula.add_argument('tipmatrfecfin', type=str, help = 'Debe elegir tipmatrfecini', required = True)
parseModificarTipoMatricula.add_argument('tipmatrcosto', type=int, help = 'Debe elegir tipmatrcosto', required = True)
parseModificarTipoMatricula.add_argument('tipmatrusumod', type=str, help = 'Debe elegir tipmatrusumod', required = True)
parseModificarTipoMatricula.add_argument('tipmatrdescripcion', type=str, help = 'Debe elegir tipmatrdescripcion')
class ModificarTipoMatricula(Resource):
  def post(self):
    data = parseModificarTipoMatricula.parse_args()
    return modificarTipoMatricula(data)
  
  
parseGestionarTipoMatriculaEstado = reqparse.RequestParser()
parseGestionarTipoMatriculaEstado.add_argument('tipo', type=int, help = 'Debe elegir tipo', required = True)  
parseGestionarTipoMatriculaEstado.add_argument('tipmatrid', type=int, help = 'Debe elegir tipmatrid', required = True)  
parseGestionarTipoMatriculaEstado.add_argument('tipmatrusumod', type=str, help = 'Debe elegir tipmatrusumod', required = True)
class GestionarTipoMatriculaEstado(Resource):
  def post(self):
    data = parseGestionarTipoMatriculaEstado.parse_args()
    return gestionarTipoMatriculaEstado(data)


parseInsertarMatricula = reqparse.RequestParser()
parseInsertarMatricula.add_argument('tipmatrid', type=int, help = 'Debe elegir tipmatrid', required = True)
parseInsertarMatricula.add_argument('matrfec', type=str, help = 'Debe elegir matrfec', required = True)
parseInsertarMatricula.add_argument('peridestudiante', type=int, help = 'Debe elegir peridestudiante', required = True)
parseInsertarMatricula.add_argument('pagoidmatricula', type=int, help = 'Debe elegir pagoidmatricula')
parseInsertarMatricula.add_argument('matrusureg', type=str, help = 'Debe elegir matrusureg', required = True)
parseInsertarMatricula.add_argument('matrdescripcion', type=str, help = 'Debe elegir matrdescripcion')
class InsertarMatricula(Resource):
  def post(self):
    data = parseInsertarMatricula.parse_args()
    return insertarMatricula(data)
  
parseModificarMatricula = reqparse.RequestParser()
parseModificarMatricula.add_argument('matrid', type=int, help = 'Debe elegir matrid', required = True)
parseModificarMatricula.add_argument('tipmatrid', type=int, help = 'Debe elegir tipmatrid', required = True)
parseModificarMatricula.add_argument('matrfec', type=str, help = 'Debe elegir matrgestion', required = True)
parseModificarMatricula.add_argument('peridestudiante', type=int, help = 'Debe elegir peridestudiante', required = True)
parseModificarMatricula.add_argument('matrusumod', type=str, help = 'Debe elegir matrusureg', required = True)
parseModificarMatricula.add_argument('matrdescripcion', type=str, help = 'Debe elegir matrdescripcion')
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