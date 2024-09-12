from psycopg2 import sql
from core.database import execute, execute, as_string
from models.rol_model import Rol
from flask import jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from datetime import datetime

# Role's function

def getRoles(): 
    try:
        roles = Rol.query.order_by(Rol.rolid).all()
        _data = [rol.to_dict() for rol in roles]
       
        response_data = {
            "message": "Data recovered successfully",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def manageRole(data):
    type = data.get("tipo")
    if type == 1:
        return createRole(data)
    elif type == 2:
        rolid = data.get("rolid")
        return updateRole(data, rolid)
    elif type == 3:
        rolid = data.get("rolid")
        return deleteRole(rolid)
    else:
        return {'code': 400, 'message': 'Invalid operation type'}, 400


def createRole(data):
    try:
        existe = db.session.query(Rol).filter_by(rolnombre=data["rolnombre"]).first()
        if existe:
            error_response = {
                "error": "Duplicate entry",
                "message": "A role with the same name already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        rol = Rol(
            rolnombre=data["rolnombre"],
            roldescripcion=data["roldescripcion"],
            rolusureg=data["rolusureg"],
            rolfecreg=datetime.now(),
            rolusumod=data["rolusureg"],
            rolfecmod=datetime.now(),
            rolestado=data["rolestado"]
        )
        db.session.add(rol)
        db.session.commit()
        _data = rol.to_dict()

        response_data = {
            "message": "Rol created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.rol_model import db, Rol
def updateRole(data, rolid):
    try:
        rol = Rol.query.filter_by(rolid=rolid).first()
        if not rol:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        rol.rolnombre = data["rolnombre"]
        rol.roldescripcion = data["roldescripcion"]
        rol.rolusumod = data["rolusumod"]
        rol.rolfecmod = datetime.now()
        rol.rolestado = data["rolestado"]

        db.session.commit()
        _data = rol.to_dict()
        response_data = {
                "message": "Rol updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
            }
        response = make_response(jsonify(response_data), HTTPStatus.OK)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteRole(rolid):
    try:
        rol = Rol.query.filter_by(rolid=rolid).first()
        if not rol:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(rol)
        db.session.commit()
        response_data = {
            "message": "Rol deleted successfully",
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def manageRoleStatus(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_rol_gestionar_estado({tipo}, {rolid}, {rolusumod});
            ''').format(
                tipo=sql.Literal(data['tipo']),
                rolid=sql.Literal(data['rolid']),
                rolusumod=sql.Literal(data['rolusumod'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print("Error en Gestionar Rol Estado: ", err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result
