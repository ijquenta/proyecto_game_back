from flask_restful import Resource, reqparse
from http import HTTPStatus
import services.reportes_service as reporte

parseRptBenSoc = reqparse.RequestParser()
parseRptBenSoc.add_argument('idGestion',type=int , help = 'This field cannot be blank')
parseRptBenSoc.add_argument('idMes',type=int , help = 'This field cannot be blank')
parseRptBenSoc.add_argument('codDocente',type=str , help = 'This field cannot be blank')
parseRptBenSoc.add_argument('nroLiquidacion',type=str , help = 'This field cannot be blank')
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