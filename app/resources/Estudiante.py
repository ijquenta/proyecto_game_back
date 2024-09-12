from flask_restful import Resource, reqparse
from resources.Autenticacion import token_required
from services.estudiante_service import * # Servicio de estudiante
from resources.Autenticacion import token_required

class ListarEstudiante(Resource):
    @token_required
    def get(self):
        return listarEstudiante()
      

parseObtenerMateriasInscritas = reqparse.RequestParser()
parseObtenerMateriasInscritas.add_argument('perid', type=int, help='Ingresar perid', required=True)
class ObtenerMateriasInscritas(Resource):
    @token_required
    def post(self):
        data = parseObtenerMateriasInscritas.parse_args()
        return obtenerMateriasInscritas(data)

parseActualizarDatosPersonales = reqparse.RequestParser()
parseActualizarDatosPersonales.add_argument('perid', type=int, help='ID de la persona - perid', required=True)
parseActualizarDatosPersonales.add_argument('pernrohijos', type=int, help='número de hijos - pernrohijos', required=True)
parseActualizarDatosPersonales.add_argument('perprofesion', type=str, help='Profesión - perprofesion', required=True)
parseActualizarDatosPersonales.add_argument('perfeclugconversion', type=str, help='Fecha, lugar de conversion - perfeclugconversion', required=True)
parseActualizarDatosPersonales.add_argument('perbautismoaguas', type=int, help='Bautismo en aguas - perbautismoaguas', required=True)
parseActualizarDatosPersonales.add_argument('perbautismoespiritu', type=int, help='Bautismo en espiritu - perbautismoespiritu', required=True)
parseActualizarDatosPersonales.add_argument('pernomdiriglesia', type=str, help='Nombre y dirección de la iglesia - pernomdiriglesia', required=True)
parseActualizarDatosPersonales.add_argument('pernompastor', type=str, help='Nombre del pastor - pernompastor', required=True)
parseActualizarDatosPersonales.add_argument('perusumod', type=str, help='Usuario que modificó la persona - perusumod', required=True)
class ActualizarDatosPersonales(Resource):
    @token_required
    def post(self):
        data = parseActualizarDatosPersonales.parse_args()
        return actualizarDatosPersonales(data)  
    
    
parseGetInformacionDocente = reqparse.RequestParser()
parseGetInformacionDocente.add_argument('perid', type=int, help='Ingresar perid', required=True)
class GetInformacionDocente(Resource):
    @token_required
    def post(self):
        data = parseGetInformacionDocente.parse_args()
        return getInformacionDocente(data)