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

parseRptParamAFP = reqparse.RequestParser()
parseRptParamAFP.add_argument('idGestion',type=int , help = 'This field cannot be blank')
parseRptParamAFP.add_argument('idMes',type=int , help = 'This field cannot be blank')
parseRptParamAFP.add_argument('username',type=str , help = 'This field cannot be blank')
class rptHaberesAportes(Resource):
    def post(self):
        data = parseRptParamAFP.parse_args()
        return reporte.rptHaberesAportes(data['idGestion'], data['idMes'], 0, data['username'])
"""