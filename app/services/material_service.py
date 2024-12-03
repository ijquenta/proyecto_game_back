from http import HTTPStatus
from flask import jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
from models.texto_model import Texto, db
from flask import jsonify, make_response
from sqlalchemy import select

def getListTextoCombo():
    try:
        # Ejecutar la consulta
        query = db.session.execute('''
            select distinct t.texid, t.texnombre 
            from academico.texto t
            where t.texestado = 1
            order by t.texnombre       
        ''')
        
        # Obtener los resultados en una lista de diccionarios
        resultados = [{"texid": row.texid, "texnombre": row.texnombre} for row in query]
        
        # Devolver la respuesta en formato JSON
        return make_response(jsonify(resultados), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }