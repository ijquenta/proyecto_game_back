from flask_restful import Resource
from flask import session
from resources.Autenticacion import token_required
from client.responses import clientResponses as messages

class Index(Resource):
  def get(self):
    print (session)
    return messages.index

class Protected(Resource):
  @token_required
  def get(self):
    print (session)
    return messages.protected