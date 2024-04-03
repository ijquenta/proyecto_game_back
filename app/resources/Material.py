from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
from http import HTTPStatus
# from services.beneficio_service import *
# from resources.Autenticacion import token_required
from services.material_service import listarMaterial, listarTexto, insertarTexto

class ListarMaterial(Resource):
    # @token_required
    def get(self):
        return listarMaterial()

class ListarTexto(Resource):
    # @token_required
    def get(self):
        return listarTexto()

# Insertar Texto
parseInsertarTexto = reqparse.RequestParser()
parseInsertarTexto.add_argument('texnombre', type=str, help='Ingrese textnombre', required=True)
parseInsertarTexto.add_argument('textipo', type=str, help='Ingrese textipo', required=True)
parseInsertarTexto.add_argument('texdocumento', type=str, help='Ingrese texdocumento', required=True)
parseInsertarTexto.add_argument('texusureg', type=str, help='Ingrese textusureg', required=True)
class InsertarTexto(Resource):
    # @token_required
    def post(self):
        data = parseInsertarTexto.parse_args()
        return insertarTexto(data)