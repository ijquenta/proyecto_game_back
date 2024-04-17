from flask_restful import Resource, reqparse
from flask import session, request
from client.responses import clientResponses as messages
from core.auth import *
from http import HTTPStatus
from services.beneficio_service import *
from services.rol_service import *
from functools import wraps
from flask import request

parseGestionarRol = reqparse.RequestParser()
parseGestionarRol.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)
parseGestionarRol.add_argument('rolid', type=int, help='Debe elegir rolid', required=True)
parseGestionarRol.add_argument('rolnombre', type=str, help='Debe elegir rolnombre', required=True)
parseGestionarRol.add_argument('roldescripcion', type=str, help='Debe elegir roldescripcion', required=True)
parseGestionarRol.add_argument('rolestado', type=int, help='Debe elegir rolestado', required=True)
parseGestionarRol.add_argument('rolusureg', type=str, help='Debe elegir rolusureg', required=True)
class GestionarRol(Resource):
  def post(self):
    data = parseGestionarRol.parse_args()
    return gestionarRol(data)
  
parseGestionarRolEstado = reqparse.RequestParser()
parseGestionarRolEstado.add_argument('tipo', type=int, help='Debe elegir tipo', required=True)  
parseGestionarRolEstado.add_argument('rolid', type=int, help='Debe elegir rolid', required=True)  
parseGestionarRolEstado.add_argument('rolusumod', type=str, help='Debe elegir rolusumod', required=True)
class GestionarRolEstado(Resource):
  def post(self):  
    data = parseGestionarRolEstado.parse_args()
    return gestionarRolEstado(data)

class ListarRoles(Resource):
  def get(self):
      return listarRoles()

parseCrearRol = reqparse.RequestParser()
parseCrearRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseCrearRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseCrearRol.add_argument('rolUsuReg', type=str, help = 'Debe elegir el usuario de registro')
class CrearRol(Resource):
  def post(self):
      data = parseCrearRol.parse_args()
      return crearRol(data)
  
parseModificarRol = reqparse.RequestParser()
parseModificarRol.add_argument('rolId', type=int, help = 'Debe elegir el Id del rol', required = True)
parseModificarRol.add_argument('rolNombre', type=str, help = 'Debe elegir el nombre del rol', required = True)
parseModificarRol.add_argument('rolDescripcion', type=str, help = 'Debe elegir la Descripción del rol', required = True)
parseModificarRol.add_argument('rolUsuMod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class ModificarRol(Resource):
  def post(self):
      data = parseModificarRol.parse_args()
      return modificarRol(data)
  
parseEliminarRol = reqparse.RequestParser()
parseEliminarRol.add_argument('rolid', type=str, help = 'Debe elegir el Id del rol', required = True)
parseEliminarRol.add_argument('rolusumod', type=str, help = 'Debe elegir el usuario de registro', required = True)
class EliminarRol(Resource):
  def post(self):
      data = parseEliminarRol.parse_args()
      return eliminarRol(data)

