from flask_restful import Resource, reqparse
from services.material_service import * # Servicio de material de apoyo
from resources.Autenticacion import token_required

class GetListTextoCombo(Resource):
    @token_required
    def get(self):
      return getListTextoCombo()
