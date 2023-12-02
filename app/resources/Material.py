from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
from http import HTTPStatus
from services.beneficio_service import *
from resources.Autenticacion import token_required
from services.material_service import *

class ListarMaterial(Resource):
    # @token_required
    def get(self):
        return listarMaterial()
     