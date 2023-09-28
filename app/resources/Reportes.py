from flask_restful import Resource, reqparse
from http import HTTPStatus
import services.reportes_service as reporte

"""
parseRptParam = reqparse.RequestParser()
# parseRptParam.add_argument('partida',type=str , help = 'This field cannot be blank')
parseRptParam.add_argument('idGestion',type=int , help = 'This field cannot be blank')
parseRptParam.add_argument('partida',type=int , help = 'This field cannot be blank')
parseRptParam.add_argument('username',type=str , help = 'This field cannot be blank')
class RptHaberesDescuentos(Resource):
    def post(self):
        data = parseRptParam.parse_args()
        return reporte.rptHaberesDescuentos(data['idGestion'], data['partida'], data['username'])

class RptHaberesBorrador(Resource):
    def post(self):
        data = parseRptParam.parse_args()
        return reporte.rptHaberesBorrador(data['idGestion'], data['partida'], data['username'])

class RptHaberesResumen(Resource):
    def post(self):
        data = parseRptParam.parse_args()
        return reporte.rptHaberesResumen(data['idGestion'], data['partida'], data['username'])

class RptHaberesExAdministrativos(Resource):
    def post(self):
        data = parseRptParam.parse_args()
        return reporte.rptHaberesExAdministrativos(data['idGestion'], data['partida'], data['username'])

class RptHaberesResumenExAdministrativos(Resource):
    def post(self):
        data = parseRptParam.parse_args()
        return reporte.rptHaberesResumenExAdministrativos(data['idGestion'], data['partida'], data['username'])
class RptPersonalExcluido(Resource):
    def post(self):
        data = parseRptParam.parse_args()
        return reporte.rptPersonalExcluido(data['idGestion'], data['partida'], data['username'])
"""

parseRptBenSoc = reqparse.RequestParser()
parseRptBenSoc.add_argument('idGestion',type=int , help = 'This field cannot be blank')
parseRptBenSoc.add_argument('idMes',type=int , help = 'This field cannot be blank')
parseRptBenSoc.add_argument('codDocente',type=str , help = 'This field cannot be blank')
parseRptBenSoc.add_argument('nroLiquidacion',type=str , help = 'This field cannot be blank')
# parseRptBenSoc.add_argument('username',type=str , help = 'This field cannot be blank')
class rptBeneficioSocial(Resource):
    def post(self):
        data = parseRptBenSoc.parse_args()
        return reporte.rptBeneficoSocial(data['idGestion'], data['idMes'], data['codDocente'], data['nroLiquidacion'])
class rptReintegroBeneficioSocial(Resource):
    def post(self):
        data = parseRptBenSoc.parse_args()
        return reporte.rptReintegroBeneficoSocial(data['idGestion'], data['idMes'], data['codDocente'], data['nroLiquidacion'])
class rptConsolidadoBeneficioSocial(Resource):
    def post(self):
        data = parseRptBenSoc.parse_args()
        return reporte.rptConsolidadoBeneficoSocial(data['idGestion'], data['idMes'], data['codDocente'], data['nroLiquidacion'])


parseRptTotalesSigma = reqparse.RequestParser()
parseRptTotalesSigma.add_argument('fechaInicio', type=str, help='this field cannot be black')
parseRptTotalesSigma.add_argument('fechaFin', type=str, help='this fild cannot be black')
class rptTotalesSigma(Resource):
    def post(self):
        data = parseRptTotalesSigma.parse_args()
        return reporte.rptTotalesSigma()