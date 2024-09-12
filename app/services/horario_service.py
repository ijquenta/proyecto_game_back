import hashlib
from http import HTTPStatus
from flask import jsonify, make_response
from utils.date_formatting import *
from sqlalchemy.exc import SQLAlchemyError
from core.database import db
from datetime import datetime


# Importaciones
from flask import jsonify, make_response, request
from models.horario_model import Horario, db

def getHorarios():
    try:
        # Obtener todos los horarios
        horarios = Horario.query.all()
        # Convertir los objetos Horario a diccionarios
        horarios_dict = [horario.to_dict() for horario in horarios]
        return make_response(jsonify(horarios_dict), HTTPStatus.OK)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)


def getHorariosByCursoMateria(curmatid):
    try:
        # Obtener el horario por curmatid
        horarios = Horario.query.filter_by(curmatid=curmatid).all()
        if horarios:
            # Convertir cada objeto Horario a un diccionario
            horarios_dict = [horario.to_dict() for horario in horarios]
            return make_response(jsonify(horarios_dict), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Horario no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)


def createHorario(data):
    try:
        nuevo_horario = Horario(
            curmatid=data['curmatid'],
            hordia=data['hordia'],
            horini=datetime.strptime(data['horini'], '%H:%M:%S').time(),
            horfin=datetime.strptime(data['horfin'], '%H:%M:%S').time(),
            horfecini=datetime.strptime(data['horfecini'], '%Y-%m-%d').date(),
            horfecfin=datetime.strptime(data['horfecfin'], '%Y-%m-%d').date(),
            horusureg=data['horusureg'],
            horfecreg=datetime.utcnow(),
            horusumod=data['horusureg'],
            horfecmod=datetime.utcnow(),
            horestado=1
        )
        db.session.add(nuevo_horario)
        db.session.commit()
        return make_response(jsonify({'message': 'Horario creado correctamente'}), HTTPStatus.CREATED)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
    
from models.horario_model import Horario, db   
    
def updateHorario(data, horid):
    try:
        horario = Horario.query.get(horid)
        if horario:
            horario.hordia = data['hordia']
            horario.horini = datetime.strptime(data['horini'], '%H:%M:%S').time()
            horario.horfin = datetime.strptime(data['horfin'], '%H:%M:%S').time()
            horario.horfecini = datetime.strptime(data['horfecini'], '%Y-%m-%d').date()
            horario.horfecfin = datetime.strptime(data['horfecfin'], '%Y-%m-%d').date()
            horario.horusumod = data['horusumod']
            horario.horfecmod = datetime.utcnow()
            db.session.commit()
            return make_response(jsonify({'message': 'Horario actualizado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Horario no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def deleteHorario(horid):
    try:
        horario = Horario.query.get(horid)
        if horario:
            db.session.delete(horario)
            db.session.commit()
            return make_response(jsonify({'message': 'Horario eliminado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Horario no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
    
    
def getHorariosPorCurmatid(curmatid):
    try:
        # Realiza la consulta a la base de datos
        horarios = db.session.query(Horario).filter(Horario.curmatid == curmatid).all()

        # Verifica si se encontraron resultados
        if not horarios:
            return make_response(jsonify({"error": "No se encontraron horarios para este curmatid"}), HTTPStatus.NOT_FOUND)

        # Mapea los resultados a un diccionario para devolver como JSON
        resultado = [
            {
                'horid': horario.horid,
                'curmatid': horario.curmatid,
                'hordia': horario.hordia,
                'horini': str(horario.horini),  # Convierte a string si es necesario
                'horfin': str(horario.horfin),  # Convierte a string si es necesario
                'horfecini': horario.horfecini.isoformat() if horario.horfecini else None,
                'horfecfin': horario.horfecfin.isoformat() if horario.horfecfin else None,
                'horusureg': horario.horusureg,
                'horfecreg': horario.horfecreg.isoformat() if horario.horfecreg else None,
                'horusumod': horario.horusumod,
                'horfecmod': horario.horfecmod.isoformat() if horario.horfecmod else None,
                'horestado': horario.horestado
            }
            for horario in horarios
        ]

        return make_response(jsonify(resultado), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e)
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()
