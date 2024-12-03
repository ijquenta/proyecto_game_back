from flask_restful import Resource, reqparse
import services.reportes_service as reporte # Servicio de reporte


parseRptTotalesSigma = reqparse.RequestParser()
parseRptTotalesSigma.add_argument('fechaInicio', type=str, help='this field cannot be black')
parseRptTotalesSigma.add_argument('fechaFin', type=str, help='this fild cannot be black')
class rptTotalesSigma(Resource):
    def post(self):
        data = parseRptTotalesSigma.parse_args()
        return reporte.rptTotalesSigma()
    
parseRptCursoMateriaContabilidad = reqparse.RequestParser()
parseRptCursoMateriaContabilidad.add_argument('fecini', type=str, help='Este campo es requerido fecini', required=True)
parseRptCursoMateriaContabilidad.add_argument('fecfin', type=str, help='Este campo es requerido fecfin', required=True)
parseRptCursoMateriaContabilidad.add_argument('descuentos', type=list, help='Ingrese los valores del descuentos', location='json', required=True)
parseRptCursoMateriaContabilidad.add_argument('resumen', type=list, help='Ingrese los valores del resumen', location='json', required=True)
class rptCursoMateriaContabilidad(Resource):
    def post(selft):
        data = parseRptCursoMateriaContabilidad.parse_args()
        return reporte.rptCursoMateriaContabilidad(data)
    
parseRptCursoMateriaEstudiante = reqparse.RequestParser()
parseRptCursoMateriaEstudiante.add_argument('perid', type=int, help='Este campo es requerido perid', required=True)
parseRptCursoMateriaEstudiante.add_argument('usuname', type=str, help='Este campo es requerido usuname', required=True)
class rptCursoMateriaEstudiante(Resource):
    def post(self):
        data = parseRptCursoMateriaEstudiante.parse_args()
        return reporte.rptCursoMateriaEstudiante(data)

parseRptInformacionAdmision = reqparse.RequestParser()
parseRptInformacionAdmision.add_argument('perid', type=int, help='Este campo es requerido perid', required=True)
parseRptInformacionAdmision.add_argument('usuname', type=str, help='Este campo es requerido usuname', required=True)
class RptInformacionAdmision(Resource):
    def post(self):
        data = parseRptInformacionAdmision.parse_args()
        return reporte.rptInformacionAdmision(data)