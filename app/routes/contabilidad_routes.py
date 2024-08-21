from flask_restful import Api
import resources.Contabilidad as Contabilidad
from client.routes import Routes as routes

def contabilidad_routes(api: Api):
    api.add_resource(Contabilidad.ListarCursoMateriaContabilidad, routes.listarCursoMateriaContabilidad)
    api.add_resource(Contabilidad.GetListCursoMateriaContabilidadById, routes.getListCursoMateriaContabilidadById)