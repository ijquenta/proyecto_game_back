from flask_restful import Resource, reqparse
from services.horario_service import * # Servicios  
from resources.Autenticacion import token_required # Autenticación

class GetHorarios(Resource):
    @token_required
    def get(self):
        return getHorarios()
        
class GetHorariosByCursoMateria(Resource):
    @token_required
    def get(self, curmatid):
        return getHorariosByCursoMateria(curmatid)
    
parseCreateHorario = reqparse.RequestParser()
parseCreateHorario.add_argument('curmatid', type=int, required=True, help='Ingrese curmatid')
parseCreateHorario.add_argument('hordia', type=str, required=True, help='Ingrese hordia')
parseCreateHorario.add_argument('horini', type=str, required=True, help='Ingrese horini (HH:MM:SS)')
parseCreateHorario.add_argument('horfin', type=str, required=True, help='Ingrese horfin (HH:MM:SS)')
parseCreateHorario.add_argument('horfecini', type=str, required=True, help='Ingrese horfecini (YYYY-MM-DD)')
parseCreateHorario.add_argument('horfecfin', type=str, required=True, help='Ingrese horfecfin (YYYY-MM-DD)')
parseCreateHorario.add_argument('horusureg', type=str, help='Ingrese horusureg')
class CreateHorario(Resource):
    @token_required
    def post(self):
        data = parseCreateHorario.parse_args()
        return createHorario(data)
    
parseUpdateHorario = reqparse.RequestParser()
parseUpdateHorario.add_argument('hordia', type=str, help='Ingrese hordia')
parseUpdateHorario.add_argument('horini', type=str, help='Ingrese horini (HH:MM:SS)')
parseUpdateHorario.add_argument('horfin', type=str, help='Ingrese horfin (HH:MM:SS)')
parseUpdateHorario.add_argument('horfecini', type=str, help='Ingrese horfecini (YYYY-MM-DD)')
parseUpdateHorario.add_argument('horfecfin', type=str, help='Ingrese horfecfin (YYYY-MM-DD)')
parseUpdateHorario.add_argument('horusumod', type=str, help='Ingrese horusumod')
class UpdateHorario(Resource):
    @token_required
    def put(self, horid):
        data = parseUpdateHorario.parse_args()
        return updateHorario(data, horid)
    
    
class DeleteHorario(Resource):
    @token_required
    def delete(self, horid):
        return deleteHorario(horid)
    
class GetHorariosPorCurmatid(Resource):
    @token_required
    def get(self, curmatid):
        return getHorariosPorCurmatid(curmatid)    
