from flask_restful import Resource, reqparse
from flask import session
from client.responses import clientResponses as messages
# from core.auth import require_token
from http import HTTPStatus

class Index(Resource):
  def get(self):
    print (session)
    return messages.index

class Protected(Resource):
#   @require_token()
  def get(self):
    print (session)
    return messages.protected