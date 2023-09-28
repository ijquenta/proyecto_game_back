from flask_cors import CORS
from flask import Flask, session, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from logging.handlers import RotatingFileHandler
from core import configuration
import logging
import traceback
import os

from client.responses import clientResponses as messages
from client.routes import Routes as routes

import resources.resources as resources
import resources.BenSocial as BenSocial
import resources.Persona as Persona
import resources.Reportes as Report

from core.database import Base, session_db, engine
from web.wsrrhh_service import *

# importar para JWT
from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
# importar para JWT

LOG_FILENAME = 'aplication.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=40000000, backupCount=40)
logger.addHandler(handler)


app = Flask(__name__) # Aplicación Flask
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'


def token_required(func):
	@wraps(func)
	def decorated(*args, **kwargas):
		token = request.args.get('token')
		if not token:
			return ({'Alert!':'Token is missing!'})
		try:
			payload = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'Alert':'Invalid Token'})
	return decorated

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
    	 return 'Logged in currently'
	
@app.route('/public')
def public():
	return 'For Public'

@app.route('/auth')
@token_required
def auth():return 'JWT is verified. Welcome to your dashboard'
	



@app.route('/login', methods=['POST'])
def login():
	if request.form['username'] and request.form['password'] == '123456':
		session['logged_in'] = True
		token = jwt.encode({
			'user':request.form['username'],
			'expiration': datetime.utcnow() + timedelta(seconds=120)
	    },
			app.config['SECRET_KEY'])
		return jsonify({'token': token.decode('utf-8')})
	else:
		return make_response('Unable to verify', 403, {'www-Authenticate': 'Basic realm: "Authentication Failed!'})

CORS(app)

@app.errorhandler(404)
def page_not_found(error):
    return messages._404, 404

@app.errorhandler(500)
def page_not_found(error):
    return messages._500, 500
    
api = Api(app)

app.secret_key = configuration.APP_SECRET_KEY

api.add_resource(resources.Index, routes.index)
api.add_resource(resources.Protected, routes.protected)


# API Usuarios
api.add_resource(Persona.ListarUsuarios, routes.listaUsuarios)


# Reporte Prueba
api.add_resource(Report.rptTotalesSigma, routes.rptTotalesSigma)

# Ejemplos de API
# Obtener los datos de un docente
#api.add_resource(BenSocial.ObtenerDatosDocente, routes.obtenerDatosDocente)
# Listar beneficios sociales por CodDocente
#api.add_resource(BenSocial.ListarBeneficiosDocente, routes.listarBeneficiosDocente)
#api.add_resource(BenSocial.ListarTipoMotivo, routes.listarTipoMotivo)
# Obtener los datos para modificar
#api.add_resource(BenSocial.ObtenerDatosModificar, routes.obtenerDatosModificar)
#Listar los ultimos tres meses remunerados de un docente
#api.add_resource(BenSocial.ListarTresUltimosMesesRemuneraadosDocente, routes.listarTresUltimosMesesRemuneraadosDocente)
#api.add_resource(BenSocial.RegTresUltMesRemDoc, routes.regTresUltMesRemDoc)
#api.add_resource(BenSocial.RegistrarBeneficioNuevo, routes.registrarBeneficioNuevo)
#api.add_resource(BenSocial.EliminarBeneficio, routes.eliminarBeneficio)


if __name__ == '__main__':
	Base.metadata.create_all(engine)
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print (HOST,PORT, ':3')
	app.run(host=HOST,port=PORT,debug=True)