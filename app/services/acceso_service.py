from datetime import datetime
from flask import jsonify, make_response
from models.menu_model import Menu
from core.database import db
from models.rol import Rol
from models.operacion_model import Operacion
from models.submenu_model import SubMenu
from models.acceso_model import Acceso
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from sqlalchemy.orm import aliased


def getTipoOperacion():
    try:
        # Obtener los tipos de operación de la base de datos
        tipos_operacion = Operacion.query.order_by(Operacion.openombre).all()
        # Convertir los tipos de operación en una lista de diccionarios
        response = [{"opeid": tipo.opeid, "openombre": tipo.openombre} for tipo in tipos_operacion]
        # Retornar los tipos de operación como una respuesta JSON
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        # En caso de error, devolver un mensaje de error con el código de estado correspondiente
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getAccesosv2():
    try:
        # Obtener los accesos de la base de datos
        results = db.session.query(
            Rol.rolnombre,
            SubMenu.submenid,
            SubMenu.submennombre,
            Acceso.accactivo
        ).outerjoin(SubMenu, SubMenu.submenid == Acceso.submenid)\
         .outerjoin(Rol, Rol.rolid == Acceso.rolid)\
         .distinct()\
         .order_by(Rol.rolnombre)\
         .all()
        
        # Convertir los resultados en una lista de diccionarios
        accesos = [{"rolnombre": result[0], "submenid": result[1], "submennombre": result[2], "accactivo": result[3]} for result in results]
        
        return make_response(jsonify(accesos), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def list_all_accesses():
    try:
        sm = aliased(SubMenu)
        m = aliased(Menu)
        a = aliased(Acceso)
        
        # Realizar la consulta con los joins necesarios
        accesses = (db.session.query(a, m.menicono, m.mennombre)
                    .outerjoin(sm, sm.submenid == a.submenid)
                    .outerjoin(m, m.menid == sm.menid)
                    .order_by(m.mennombre)
                    .all())

        # Convertir los accesos en una lista de diccionarios
        response = []
        for access, menicono, mennombre in accesses:
            access_dict = {col.name: getattr(access, col.name) for col in access.__table__.columns}
            access_dict["menicono"] = menicono
            access_dict["mennombre"] = mennombre
            response.append(access_dict)

        return make_response(jsonify(response), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

def getSubMenus():
    try:
        # Obtener todos los submenús de la base de datos
        submenus = SubMenu.query.order_by(SubMenu.submennombre).all()
        # Convertir los submenús en una lista de diccionarios
        response = [submenu.to_dict() for submenu in submenus]
        # Retornar la lista de submenús como una respuesta JSON
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        # En caso de error, devolver un mensaje de error con el código de estado correspondiente
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getSubMenuType():
    try:
        # Obtener todos los tipos de submenú de la base de datos
        accessType = SubMenu.query.with_entities(SubMenu.submenid, SubMenu.submennombre).order_by(SubMenu.submennombre).all()
        # Convertir los tipos de submenú en una lista de diccionarios
        response = [{"submenid": access[0], "submennombre": access[1]} for access in accessType]
        # Retornar la lista de tipos de submenú como una respuesta JSON
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        # En caso de error, devolver un mensaje de error con el código de estado correspondiente
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createAccess(data):
    try:
        acceso = Acceso(
            rolid=data['rolid'], 
            submenid=data['submenid'], 
            accactivo=data.get('accactivo', 0),
            accusureg=data['accusureg'],
            accusumod=data['accusureg'],
            accestado=data.get('accestado', 1),
            accdescripcion=data.get('accdescripcion', '')
        )
        
        db.session.add(acceso)
        db.session.commit()
        response_data = acceso.to_dict()
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


from flask import jsonify, make_response
from http import HTTPStatus
from datetime import datetime
from models.acceso_model import db, Acceso

def updateAccess(data, accid):
    try:
        access = Acceso.query.get(accid)
        
        if not access:
            return make_response(jsonify({"error": "Acceso no encontrado."}), HTTPStatus.NOT_FOUND)
        
        if 'accactivo' in data:
            access.accactivo = data['accactivo']
        if 'accusumod' in data:
            access.accusumod = data['accusumod']
        
        access.accfecmod = datetime.now()
        db.session.commit()
        response_data = access.to_dict()
        response = make_response(jsonify(response_data), HTTPStatus.OK)
        return response
        
    except Exception as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteAccess(accid):
    try:
        access = Acceso.query.get(accid)
        if not access:
            return make_response(jsonify({"error": "Acceso no encontrado."}), HTTPStatus.NOT_FOUND)
        
        db.session.delete(access)
        db.session.commit()
        response = make_response(jsonify({"message": "Acceso eliminado correctamente."}), HTTPStatus.OK)
        return response
        
    except Exception as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def getIconoNombre(submenid):
    try:
        sm = aliased(SubMenu)
        m = aliased(Menu)
        a = aliased(Acceso)
        
        result = (db.session.query(a.submenid, sm.menid, m.menicono)
                  .join(sm, sm.submenid == a.submenid)
                  .outerjoin(m, m.menid == sm.menid)
                  .filter(a.submenid == submenid)
                  .limit(1)
                  .all())

        # Convertir el resultado a una lista de diccionarios
        result_dict = [
            {
                "submenid": row.submenid,
                "menid": row.menid,
                "menicono": row.menicono
            } for row in result
        ]

        return make_response(jsonify(result_dict), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        error_response = {"error": "Error in getIconoNombre.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()