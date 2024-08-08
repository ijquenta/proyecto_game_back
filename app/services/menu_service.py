from datetime import datetime
from flask import jsonify, make_response
from core.database import db
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
# Icono Imports
from models.tipo_icono_model import TipoIcono

# Menu Imports
from models.menu_model import Menu


def getTipoIcono():
    try:
        iconos = TipoIcono.query.order_by(TipoIcono.iconombre).all()
        response = [icono.to_dict() for icono in iconos]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

# Menu Fuctions 
def getMenus():
    try:
        menus = Menu.query.order_by(Menu.mennombre).all()
        response = [menu.to_dict() for menu in menus]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def createMenu(data):
    try:
        existingMenu = db.session.query(Menu).filter_by(mennombre=data["mennombre"]).first()
        if existingMenu:
            error_response = {
                "error": "Duplicate entry",
                "message": "An menu with the same openombre already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        menu = Menu(
            mennombre=data["mennombre"],
            menicono =data["menicono"],
            menusureg=data["menusureg"],
            menusumod=data["menusureg"],
            menfecreg=datetime.now(),
            menfecmod=datetime.now(),
            menestado=data["menestado"],
            mendescripcion=data["mendescripcion"]
        )
        db.session.add(menu)
        db.session.commit()
        _data = menu.to_dict()

        response_data = {
            "message": "Menu created successfully",
            "data": _data,
            "code": HTTPStatus.OK 
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
    
    
from models.menu_model import db, Menu
def updateMenu(data, menid):
    try:
        menu = Menu.query.get(menid)
        if menu is None:
            return make_response(jsonify({"error": "Menu no founded."}), HTTPStatus.NOT_FOUND)

        menu.mennombre = data["mennombre"]
        menu.menicono  = data["menicono"]
        menu.menusumod = data["menusumod"]
        menu.menfecmod = datetime.now()
        menu.menestado = data["menestado"]
        menu.mendescripcion = data["mendescripcion"]

        db.session.commit()
        _data = menu.to_dict()
        response_data = {
            "message": "Menu updated successfully.",
            "data": _data,
            "code": HTTPStatus.OK
        }
        response = make_response(jsonify(response_data), HTTPStatus.OK)
        return response
    
    except Exception as e:
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def deleteMenu(menid):
    try:
        menu = Menu.query.get(menid)
        if menu is None:
            return make_response(jsonify({"error": "Menu no founded."}), HTTPStatus.NOT_FOUND)
        db.session.delete(menu)
        db.session.commit()
        response = make_response(jsonify({"message": "Menu deleted successfully."}), HTTPStatus.OK)
        return response
    except Exception as e:
        error_response = {"error": "Error in the database.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

