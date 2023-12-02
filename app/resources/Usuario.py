from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
from core.auth import *
from http import HTTPStatus
from services.beneficio_service import *
from services.usuario_service import *
from functools import wraps
from flask import request
from resources.Autenticacion import token_required
#import services.beneficio_service as beneficio



# @app.route('/register', methods=['POST'])


# parseLogin = reqparse.RequestParser()
# parseLogin.add_argument('email', type=str, help = 'Debe elegir el email', required = True)
# parseLogin.add_argument('password', type=str, help = 'Debe elegir la password', required = True)
# class Login(Resource):
#   print("login -->", parseLogin)
#   def post(self):
#       data = parseLogin.parse_args()
#       return login(data)


# def verify_token_middleware(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         token = request.headers['Authorization'].split(" ")[1]
#         print("token-verify-middleware-->", token)
#         return validate_token(token, output=False)
#     return wrapper




parseGestionarUsuario = reqparse.RequestParser()
parseGestionarUsuario.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseGestionarUsuario.add_argument('usuid', type=int, help='Debe elegir usuId')
parseGestionarUsuario.add_argument('perid', type=int, help='Debe elegir perId', required=True)
parseGestionarUsuario.add_argument('rolid', type=int, help='Debe elegir rolId', required=True)
parseGestionarUsuario.add_argument('usuname', type=str, help='Debe elegir usuName', required=True)
parseGestionarUsuario.add_argument('usupassword', type=str, help='Debe elegir usuPassword', required=True)
parseGestionarUsuario.add_argument('usupasswordhash', type=str, help='Debe elegir usuPasswordHash', required=True)
parseGestionarUsuario.add_argument('usuemail', type=str, help='Debe elegir usuEmail', required=True)
parseGestionarUsuario.add_argument('usuimagen', type=str, help='Debe elegir usuImagen', required=True)
parseGestionarUsuario.add_argument('usudescripcion', type=str, help='Debe elegir usuDescripcion', required=True)
parseGestionarUsuario.add_argument('usuestado', type=int, help='Debe elegir estado', required=True)
parseGestionarUsuario.add_argument('usuusureg', type=str, help='Debe elegir usuRe', required=True)
class GestionarUsuario(Resource):
  def post(self):
    data = parseGestionarUsuario.parse_args()
    print("datos Usuario: ",data)
    return gestionarUsuario(data)

class ListaUsuario(Resource):
  def get(self):
    print("ListaUsuario")
    return listaUsuario()
  
class TipoPersona(Resource):
  def get(self):
    print("TipoPersona")
    return tipoPersona()

class ListarPersona(Resource):
  # @token_required
  def get(self):
      print("ListarPersona")
      return listarPersona()

class ListarRoles(Resource):
  def get(self):
      print("Rest")
      return listarRoles()
    
parsePerfil = reqparse.RequestParser()
parsePerfil.add_argument('usuid', type=int, help = 'Debe elegir el usuid', required = True)
class Perfil(Resource):
  @token_required
  def post(self):
      data = parsePerfil.parse_args()
      return perfil(data)

parseCrearRol = reqparse.RequestParser()
parseCrearRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseCrearRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseCrearRol.add_argument('rolUsuReg', type=str, help = 'Debe elegir el usuario de registro')
class CrearRol(Resource):
  # print("CrearRol -->", parseCrearRol)
  def post(self):
      data = parseCrearRol.parse_args()
      return crearRol(data)
  
parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseModificarRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseModificarRol.add_argument('rolUsuMod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class ModificarRol(Resource):
  # print("Modificar Rol -->", parseModificarRol)
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


parseDocente = reqparse.RequestParser()
parseDocente.add_argument('nroCi', type=str, help = 'Debe elegir ci', required = True)
parseDocente.add_argument('nomCompleto', type=str, help = 'Debe elegir nombre completo', required = True)
class ObtenerDatosDocente(Resource):
  def post(self):
      data = parseDocente.parse_args()
      return obtenerDatosDocente(data['nroCi'], data['nomCompleto'])
  
  

parseBeneficios = reqparse.RequestParser()
parseBeneficios.add_argument('codDoc', type=str, help = 'Debe elegir el código del docente', required = True)
class ListarBeneficiosDocente(Resource):
  def post(self):
      data = parseBeneficios.parse_args()
      return listarBeneficiosDocente(data['codDoc'])

parseTipoMotivo = reqparse.RequestParser()
parseTipoMotivo.add_argument('codTipoMotivo', type=str, help = 'Debe elegir el código de tipo motivo')
class ListarTipoMotivo(Resource):
  def post(self):
      data = parseTipoMotivo.parse_args()
      return listarTipoMotivo()

parseListarUltimoTresMeses = reqparse.RequestParser()
parseListarUltimoTresMeses.add_argument('cod_docente', type = str, help = 'Debe elegir un codigo docente', required = True)
parseListarUltimoTresMeses.add_argument('ano', type = int, help = 'Debe elegir un año', required = True)
parseListarUltimoTresMeses.add_argument('mes', type = int, help = 'Debe elegir un mes', required = True)
class ListarTresUltimosMesesRemuneraadosDocente(Resource):
  def post(self):
    data = parseListarUltimoTresMeses.parse_args()
    return listarTresUltimosMesesRemuneraadosDocente()


parseRTUM = reqparse.RequestParser()
parseRTUM.add_argument('cod_docente', type = str, help = 'Debe elegir un codigo docente', required = True)
parseRTUM.add_argument('ano', type = int, help = 'Debe elegir un año', required = True)
parseRTUM.add_argument('mes', type = int, help = 'Debe elegir un mes', required = True)
class RegTresUltMesRemDoc(Resource):
  def post(self):
    data = parseRTUM.parse_args()
    #usuario = 1;
    return registrarTresMesesDoc(data)

parseTipoMotivo = reqparse.RequestParser()
parseTipoMotivo.add_argument('codTipoMotivo', type=str, help = 'Debe elegir el código de tipo motivo')
class ListarTipoMotivo(Resource):
  def post(self):
      data = parseTipoMotivo.parse_args()
      return listarTipoMotivo()

parseObtenerDatosModificar = reqparse.RequestParser()
parseObtenerDatosModificar.add_argument('cod_docente', type=str, help='Debe elegir el codigo del docente', required = True)
parseObtenerDatosModificar.add_argument('ano', type=int, help='Debe elegir el año de liquidación', required = True)
parseObtenerDatosModificar.add_argument('mes', type=int, help='Debe elegir el mes de liquidación', required = True)
class ObtenerDatosModificar(Resource):
  def post(self):
      data = parseObtenerDatosModificar.parse_args()
      return obtenerDatosModificar(data)




parseRegistrarBeneficioNuevo = reqparse.RequestParser()
parseRegistrarBeneficioNuevo.add_argument('ano', type=int, help='Debe elegir el año de liquidación', required = True)
parseRegistrarBeneficioNuevo.add_argument('mes', type=int, help='Debe elegir el mes de liquidación', required = True)
parseRegistrarBeneficioNuevo.add_argument('codDocente', type=str, help='Debe elegir el código del docente',required = True)
parseRegistrarBeneficioNuevo.add_argument('codTipoMotivo', type=int, help='Debe elegir un tipo de motivo', required = True) 
parseRegistrarBeneficioNuevo.add_argument('nroDictamen', type=str, help='Debe elegir numero dictamen', required = True)
parseRegistrarBeneficioNuevo.add_argument('hojaRuta', type=str, help='Debe elegir Hoja Ruta', required = True)
parseRegistrarBeneficioNuevo.add_argument('fecLiquidacion', type=str, help='Debe elegir Fecha Liquidación', required = True)
parseRegistrarBeneficioNuevo.add_argument('fecIngrec', type=str, help='Debe elegir Fecha Ingreso', required = True) 
parseRegistrarBeneficioNuevo.add_argument('fecConclusion', type=str, help='Debe elegir Fecha Conclusion', required = True)
parseRegistrarBeneficioNuevo.add_argument('fecRetiro', type=str, help='Debe elegir Fecha Retiro', required = True)
parseRegistrarBeneficioNuevo.add_argument('tsAno', type=int, help='Debe elegir tAno', required = True)
parseRegistrarBeneficioNuevo.add_argument('tsMes', type=int, help='Debe elegir tMes', required = True)
parseRegistrarBeneficioNuevo.add_argument('tsDia', type=int, help='Debe elegir tDia', required = True)
parseRegistrarBeneficioNuevo.add_argument('observaciones', type=str, help='Debe elegir una obervación', required = True)
parseRegistrarBeneficioNuevo.add_argument('usuarioReg', type=str, help='Debe elegir el usuario que modifica', required = True)
class RegistrarBeneficioNuevo(Resource):
  def post(self):
      data = parseRegistrarBeneficioNuevo.parse_args()
      return registrarBeneficioNuevo(data)

parseEliminarBeneficio = reqparse.RequestParser()
parseEliminarBeneficio.add_argument('ano', type=int, help='Debe elegir el año de liquidación', required = True)
parseEliminarBeneficio.add_argument('mes', type=int, help='Debe elegir el mes de liquidación', required = True)
parseEliminarBeneficio.add_argument('codDocente', type=str, help='Debe elegir el código del docente',required = True)
parseEliminarBeneficio.add_argument('observacion', type=str, help='Debe elegir observación',required = True)
parseEliminarBeneficio.add_argument('usuarioReg', type=str, help='Debe elegir el usuario que modifica', required = True)
class EliminarBeneficio(Resource):
  def post(self):
    data = parseEliminarBeneficio.parse_args()
    return eliminarBeneficio(data)










#Ejemplo insertar registro en base de datos
"""
parseREsP = reqparse.RequestParser()
parseREsP.add_argument('idGestion', type=int, help = 'Tiene que tener este campo', required = True)
parseREsP.add_argument('idMes', type=int, help = 'Tiene que tener este campo')
parseREsP.add_argument('idPersona', type=int, help = 'Tiene que tener este campo', required = True)
class RegRestaurarMes(Resource):
  def put(self):
    data = parseREsP.parse_args()
    return listarMesesRestaurables(data['idGestion'], data['idPersona'])
  def post(self):
    data = parseREsP.parse_args()
    usuario = 1;
    return restaurarMes(data, usuario)
"""







# parseDatoMensual = reqparse.RequestParser()
# parseDatoMensual.add_argument('apertura2', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('aperturaDescripcion', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('autoridadDescripcion', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('cargoEjecutado', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('cargoEjecutado2', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('ci', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('codAporte', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('desMes', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('descTipoTitulo', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('diasTrabajados', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('entidad', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('estudio', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('fechaAntiguedad', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('fechaFinalMensual', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('fechaInicioMensual', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idApertura', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idCargoEjecutado', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idEntidad', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idGestion', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idGradoAcademico', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idMes', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idNivelEjecutado', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idPersona', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idPlanillaRegular', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idRhaAutoridad', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idRhaPartidaEjecutado', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idRhaPmDesignacion', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idRhaTiempoEjecutado', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idRhaTipoAutoridad', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idRhaTipoDesignacion', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idTipoAportante', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idTipoIngreso', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idTipoTitulo', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('item', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('montoEvaluacion', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('montoExtra', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('montoFacturas', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('montoProfesional', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('montoSalarial', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('montoSuplencia', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('nivelEjecutadoDescripcion', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('nombreCompleto', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('nuaAfp', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('otroSueldo', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('otroSueldo1', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('otroSueldo2', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('otroSueldoIn', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('partidaEjecutado', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('porcentajeFacturas', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('puntajeEvaluacion', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('puntajeProfesional', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('puntajeSalarial', type=float, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('tiempoEjecutado', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('tipoAportante', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('tipoAutoridadDescripcion', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('tipoDesignacionDescripcion', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('tipoIngresoDescripcion', type=str, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('tipoModificacion', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idGestionProcesado', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idMesProcesado', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('correlativoLiquidacion', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('gestionLiquidacion', type=int, help = 'Tiene que tener este campo', required = True)
# parseDatoMensual.add_argument('idUsuario', type=int, help = 'Tiene que tener este campo', required = True)
# parsePRD = reqparse.RequestParser()
# parsePRD.add_argument('idPlanillaRegular', type=int, help = 'Tiene que tener este campo', required = True)
# parsePRD.add_argument('tipoModificacion', type=int, help = 'Tiene que tener este campo', required = True)
# parsePRD.add_argument('correlativoLiquidacion', type=int, help = 'Tiene que tener este campo', required = True)
# parsePRD.add_argument('gestionLiquidacion', type=int, help = 'Tiene que tener este campo', required = True)
# parsePRD.add_argument('gestionProceso', type=int, help = 'Tiene que tener este campo', required = True)
# parsePRD.add_argument('mesProceso', type=int, help = 'Tiene que tener este campo', required = True)
# class RegModificarMesPersona(Resource):
#   def post(self):
#     data = parseDatoMensual.parse_args()
#     # data['idUsuario'] = '1'
#     return modificarMes(data)
#   def put(self):
#     data = parsePRD.parse_args()
#     usuario = 1
#     return eliminarMes(data, usuario)


"""
parseDatosCalculoBS = reqparse.RequestParser()
parseDatosCalculoBS.add_argument('')
class ActualizarBeneficiosSociales(Resource):
  def post(self):
    data = parseDatosCalculoBS.parse_args()
    return modificarCalculoBS(data)
"""
