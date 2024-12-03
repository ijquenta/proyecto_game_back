from datetime import datetime
from flask import jsonify, make_response
from core.database import db
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
# Icono Imports
from models.tipo_icono_model import TipoIcono

# Menu Imports
from models.menu_model import Menu
from models.submenu_model import SubMenu


def getListSubMenu():
    try:
        # Correct query and joining
        submens = db.session.query(
            Menu.mennombre,
            SubMenu
        ).outerjoin(Menu, Menu.menid == SubMenu.menid)\
        .distinct()\
        .order_by(SubMenu.submennombre)\
        .all()

        # Properly format the response
        response = [
            {
                'mennombre': submen[0],
                'submenu': submen[1].to_dict()
            }
            for submen in submens
        ]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def createSubMenu(data):
    try:
        existingSubMenu = db.session.query(SubMenu).filter_by(submennombre=data["submennombre"]).first()
        if existingSubMenu:
            error_response = {
                "error": "Duplicate entry",
                "message": "An submenu with the same already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        submenu = SubMenu(
            submennombre=data["submennombre"],
            menid=data["menid"],
            submenusureg=data["submenusureg"],
            submenusumod=data["submenusureg"],
            submenfecreg=datetime.now(),
            submenfecmod=datetime.now(),
            submenestado=data["submenestado"],
            submendescripcion=data["submendescripcion"]
        )
        db.session.add(submenu)
        db.session.commit()
        _data = submenu.to_dict()

        response_data = {
            "message": "SubMenu created successfully",
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
    
from models.submenu_model import db, SubMenu
def updateSubMenu(data, submenid):
    try:
        submenu = SubMenu.query.get(submenid)
        if submenu is None:
            return make_response(jsonify({"error": "SubMenu no founded."}), HTTPStatus.NOT_FOUND)

        submenu.submennombre = data["submennombre"]
        submenu.menid = data["menid"]
        submenu.submenusumod = data["submenusumod"]
        submenu.submenfecmod = datetime.now()
        submenu.submenestado = data["submenestado"]
        submenu.submendescripcion = data["submendescripcion"]

        db.session.commit()
        _data = submenu.to_dict()
        response_data = {
            "message": "SubMenu updated successfully.",
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
    
def deleteSubMenu(submenid):
    try:
        submenu = SubMenu.query.get(submenid)
        if submenu is None:
            return make_response(jsonify({"error": "SubMenu no founded."}), HTTPStatus.NOT_FOUND)
        db.session.delete(submenu)
        db.session.commit()
        response = make_response(jsonify({"message": "SubMenu deleted successfully."}), HTTPStatus.OK)
        return response
    except Exception as e:
        error_response = {"error": "Error in the database.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def getTipoMenu():
    try:
        tipoMenu = Menu.query.order_by(Menu.mennombre).all()
        response = [{"menid": tipmen.menid, "mennombre": tipmen.mennombre} for tipmen in tipoMenu]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
