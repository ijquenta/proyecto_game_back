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

from core.database import Base, session_db, engine

from web.wsrrhh_service import *

LOG_FILENAME = 'aplication.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=40000000, backupCount=40)
logger.addHandler(handler)


app = Flask(__name__)
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

# Obtener los datos de un docente
api.add_resource(BenSocial.ObtenerDatosDocente, routes.obtenerDatosDocente)

# Listar beneficios sociales por CodDocente
api.add_resource(BenSocial.ListarBeneficiosDocente, routes.listarBeneficiosDocente)

api.add_resource(BenSocial.ListarTipoMotivo, routes.listarTipoMotivo)

# Obtener los datos para modificar
api.add_resource(BenSocial.ObtenerDatosModificar, routes.obtenerDatosModificar)


#Listar los ultimos tres meses remunerados de un docente
api.add_resource(BenSocial.ListarTresUltimosMesesRemuneraadosDocente, routes.listarTresUltimosMesesRemuneraadosDocente)

api.add_resource(BenSocial.RegTresUltMesRemDoc, routes.regTresUltMesRemDoc)

api.add_resource(BenSocial.RegistrarBeneficioNuevo, routes.registrarBeneficioNuevo)

api.add_resource(BenSocial.EliminarBeneficio, routes.eliminarBeneficio)


#Modificar beneficios sociales
# api.add_resource(BenSocial.ActualizarBeneficiosSociales, routes.actualizarBeneficiosSociales)
#Exemplo insertar en base de datos
#api.add_resource(PlaRegular.RegRestaurarMes, routes.regRestaurarMes)

datos_de_prueba = [
        {
            'cod_docente': 'DOC001',
            'uni_ejecutora': '05',
            'ano': 2023,
            'mes': 10,
            'tg_ano': 0,
            'tg_mes': 0
        },
        {
            'cod_docente': 'DOC001',
            'uni_ejecutora': '05',
            'ano': 2023,
            'mes': 9,
            'tg_ano': 0,
            'tg_mes': 0
        },
        {
            'cod_docente': 'DOC001',
            'uni_ejecutora': '05',
            'ano': 2023,
            'mes': 8,
            'tg_ano': 0,
            'tg_mes': 0
        }
    ]
# print(insertarTresUltimosMeses(datos_de_prueba)
# print(resultado)
	
if __name__ == '__main__':
	Base.metadata.create_all(engine)
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print (HOST,PORT, 'xD')
	app.run(host=HOST,port=PORT,debug=True)