from flask_restful import Api
import resources.Horario_resource as Horario_resource
from client.routes import Routes as routes

def horario_routes(api: Api):
    api.add_resource(Horario_resource.GetHorarios, routes.getHorarios)                                                                  
    api.add_resource(Horario_resource.GetHorariosByCursoMateria, routes.getHorariosByCursoMateria)
    api.add_resource(Horario_resource.CreateHorario, routes.createHorario)
    api.add_resource(Horario_resource.UpdateHorario, routes.updateHorario)
    api.add_resource(Horario_resource.DeleteHorario, routes.deleteHorario)
    api.add_resource(Horario_resource.GetHorariosPorCurmatid, routes.getHorariosPorCurmatid)