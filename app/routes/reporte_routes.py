from flask_restful import Api
import resources.Reportes as Report
from client.routes import Routes as routes

def reporte_routes(api: Api):
    api.add_resource(Report.rptTotalesSigma, routes.rptTotalesSigma)
    api.add_resource(Report.rptCursoMateriaContabilidad, routes.rptCursoMateriaContabilidad)
    api.add_resource(Report.RptInformacionAdmision, routes.rptInformacionAdmision)