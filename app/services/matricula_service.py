# Importaciones estándar de Python
from http import HTTPStatus

# Importaciones de Flask
from flask import jsonify, make_response

# Importaciones de SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError

# Importaciones del core del proyecto
from core.database import select, execute_function

# Importaciones de modelos
from models.matricula_model import Matricula
from models.persona_model import Persona
from models.pago_model import Pago
from models.tipo_matricula_model import TipoMatricula, db

# Importaciones de utilidades
from utils.date_formatting import *

def listarMatriculaEstudiante(perid):
    try:
        # Definir alias para las tablas si es necesario
        Estudiante = aliased(Persona)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    Matricula.matrid,
                    Matricula.matrfec,
                    Matricula.tipmatrid,
                    TipoMatricula.tipmatrgestion,
                    TipoMatricula.tipmatrfecini,
                    TipoMatricula.tipmatrfecfin,
                    TipoMatricula.tipmatrcosto,
                    Matricula.peridestudiante,
                    Estudiante.pernomcompleto.label('pernomcompleto'),
                    Estudiante.pernrodoc.label('pernrodoc'),
                    Estudiante.perfoto.label('perfoto'),
                    Matricula.pagoidmatricula,
                    Pago.pagdescripcion,
                    Pago.pagmonto,
                    Pago.pagarchivo,
                    Pago.pagfecha,
                    Pago.pagtipo,
                    Pago.pagestado,
                    Matricula.matrusureg,
                    Matricula.matrfecreg,
                    Matricula.matrusumod,
                    Matricula.matrfecmod,
                    Matricula.matrestado,
                    Matricula.matrdescripcion
                )
                .join(Estudiante, Matricula.peridestudiante == Estudiante.perid)
                .outerjoin(Pago, Matricula.pagoidmatricula == Pago.pagid)
                .join(TipoMatricula, Matricula.tipmatrid == TipoMatricula.tipmatrid)
                .filter(Matricula.peridestudiante == perid)
                .all())

        # Convertir los resultados en una lista de diccionarios con fechas formateadas
        response_data = [
            {
                "matrid": row.matrid,
                "matrfec": row.matrfec.isoformat() if row.matrfec else None,
                "tipmatrid": row.tipmatrid,
                "tipmatrgestion": row.tipmatrgestion,
                "tipmatrfecini": row.tipmatrfecini.isoformat() if row.tipmatrfecini else None,
                "tipmatrfecfin": row.tipmatrfecfin.isoformat() if row.tipmatrfecfin else None,
                "tipmatrcosto": row.tipmatrcosto,
                "peridestudiante": row.peridestudiante,
                "pernomcompleto": row.pernomcompleto,
                "pernrodoc": row.pernrodoc,
                "perfoto": row.perfoto,
                "pagoidmatricula": row.pagoidmatricula,
                "pagdescripcion": row.pagdescripcion,
                "pagmonto": row.pagmonto,
                "pagarchivo": row.pagarchivo,
                "pagfecha": row.pagfecha.isoformat() if row.pagfecha else None,
                "pagtipo": row.pagtipo,
                "pagestado": row.pagestado,
                "matrusureg": row.matrusureg,
                "matrfecreg": row.matrfecreg.isoformat() if row.matrfecreg else None,
                "matrusumod": row.matrusumod,
                "matrfecmod": row.matrfecmod.isoformat() if row.matrfecmod else None,
                "matrestado": row.matrestado,
                "matrdescripcion": row.matrdescripcion
            } for row in query
        ]

        # Crear la respuesta con los datos obtenidos
        return make_response(jsonify({
            "message": "Matrículas obtenidas con éxito",
            "data": response_data,
            "code": HTTPStatus.OK
        }), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        # Manejar cualquier error de SQLAlchemy
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

def listarMatricula():
    """
    Lista todas las matrículas con los detalles relacionados de las tablas asociadas.

    Esta función realiza una consulta a la base de datos para obtener todas las matrículas
    junto con los detalles de las tablas relacionadas como `Persona`, `Pago`, y `TipoMatricula`.

    Returns:
        Response: Una respuesta JSON con un mensaje de éxito y los datos de las matrículas, o un 
        mensaje de error si ocurre una excepción.
    """
    try:
        # Definir alias para las tablas si es necesario
        Estudiante = aliased(Persona)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    Matricula.matrid,
                    Matricula.matrfec,
                    Matricula.tipmatrid,
                    TipoMatricula.tipmatrgestion,
                    TipoMatricula.tipmatrfecini,
                    TipoMatricula.tipmatrfecfin,
                    TipoMatricula.tipmatrcosto,
                    Matricula.peridestudiante,
                    Estudiante.pernomcompleto.label('pernomcompleto'),
                    Estudiante.pernrodoc.label('pernrodoc'),
                    Estudiante.perfoto.label('perfoto'),
                    Matricula.pagoidmatricula,
                    Pago.pagdescripcion,
                    Pago.pagmonto,
                    Pago.pagarchivo,
                    Pago.pagfecha,
                    Pago.pagtipo,
                    Pago.pagestado,
                    Matricula.matrusureg,
                    Matricula.matrfecreg,
                    Matricula.matrusumod,
                    Matricula.matrfecmod,
                    Matricula.matrestado,
                    Matricula.matrdescripcion
                )
                .join(Estudiante, Matricula.peridestudiante == Estudiante.perid)
                .outerjoin(Pago, Matricula.pagoidmatricula == Pago.pagid)
                .join(TipoMatricula, Matricula.tipmatrid == TipoMatricula.tipmatrid)
                .all())

        # Convertir los resultados en una lista de diccionarios con fechas formateadas
        response_data = [
            {
                "matrid": row.matrid,
                "matrfec": row.matrfec.isoformat() if row.matrfec else None,
                "tipmatrid": row.tipmatrid,
                "tipmatrgestion": row.tipmatrgestion,
                "tipmatrfecini": row.tipmatrfecini.isoformat() if row.tipmatrfecini else None,
                "tipmatrfecfin": row.tipmatrfecfin.isoformat() if row.tipmatrfecfin else None,
                "tipmatrcosto": row.tipmatrcosto,
                "peridestudiante": row.peridestudiante,
                "pernomcompleto": row.pernomcompleto,
                "pernrodoc": row.pernrodoc,
                "perfoto": row.perfoto,
                "pagoidmatricula": row.pagoidmatricula,
                "pagdescripcion": row.pagdescripcion,
                "pagmonto": row.pagmonto,
                "pagarchivo": row.pagarchivo,
                "pagfecha": row.pagfecha.isoformat() if row.pagfecha else None,
                "pagtipo": row.pagtipo,
                "pagestado": row.pagestado,
                "matrusureg": row.matrusureg,
                "matrfecreg": row.matrfecreg.isoformat() if row.matrfecreg else None,
                "matrusumod": row.matrusumod,
                "matrfecmod": row.matrfecmod.isoformat() if row.matrfecmod else None,
                "matrestado": row.matrestado,
                "matrdescripcion": row.matrdescripcion
            } for row in query
        ]

        # Crear la respuesta con los datos obtenidos
        return make_response(jsonify({
            "message": "Matrículas obtenidas con éxito",
            "data": response_data,
            "code": HTTPStatus.OK
        }), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        # Manejar cualquier error de SQLAlchemy
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()



def insertarMatricula(data):
    return execute_function(f'''
    SELECT academico.f_matricula_insertar(
          {data['tipmatrid']},
        \'{data['matrfec']}\',
          {data['peridestudiante']},
          NULL,
        \'{data['matrusureg']}\',
        \'{data['matrdescripcion']}\')  as valor;    
                            ''')
def modificarMatricula(data):
    print("data-modificar-matricula:::", data)
    return execute_function(f'''
    SELECT academico.f_matricula_modificar(
          {data['matrid']},
          {data['tipmatrid']},
        \'{data['matrfec']}\',
          {data['peridestudiante']},
        \'{data['matrusumod']}\',
        \'{data['matrdescripcion']}\')  as valor;
    ''')   

def gestionarMatriculaEstado(data):
    return execute_function(f'''
    SELECT academico.f_matricula_gestionar_estado(
          {data['tipo']}, 
          {data['matrid']}, 
        \'{data['matrusumod']}\')  as valor;                      
    ''')  
"""
def listarTipoMatricula():
    lista = select(f''' 
                  SELECT tipmatrid, tipmatrgestion, tipmatrfecini, tipmatrfecfin, 
                         tipmatrcosto, tipmatrusureg, tipmatrfecreg, tipmatrusumod,
                         tipmatrfecmod, tipmatrestado, tipmatrdescripcion 
                  FROM academico.tipo_matricula 
                  --    WHERE tipmatrestado = 1
                  ORDER BY tipmatrid;
                  ''')
    for l in lista:
        l['tipmatrfecini'] = darFormatoFechaSinHora(l['tipmatrfecini'])
        l['tipmatrfecfin'] = darFormatoFechaSinHora(l['tipmatrfecfin'])
        l['tipmatrfecreg'] = darFormatoFechaConHora(l['tipmatrfecreg'])
        l['tipmatrfecmod'] = darFormatoFechaConHora(l['tipmatrfecmod'])
    return lista
"""
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, make_response
from http import HTTPStatus
from models.tipo_matricula_model import TipoMatricula, db
def listarTipoMatricula():
    """
    Lista todos los registros de la tabla `TipoMatricula` con los detalles asociados.

    Esta función realiza una consulta a la base de datos para obtener todos los registros
    de la tabla `TipoMatricula` y formatea las fechas antes de devolver la respuesta.

    Returns:
        Response: Una respuesta JSON con un mensaje de éxito y los datos de los tipos de matrícula,
        o un mensaje de error si ocurre una excepción.
    """
    try:
        # Realizar la consulta
        query = (db.session.query(
                    TipoMatricula.tipmatrid,
                    TipoMatricula.tipmatrgestion,
                    TipoMatricula.tipmatrfecini,
                    TipoMatricula.tipmatrfecfin,
                    TipoMatricula.tipmatrcosto,
                    TipoMatricula.tipmatrusureg,
                    TipoMatricula.tipmatrfecreg,
                    TipoMatricula.tipmatrusumod,
                    TipoMatricula.tipmatrfecmod,
                    TipoMatricula.tipmatrestado,
                    TipoMatricula.tipmatrdescripcion
                )
                # .filter(TipoMatricula.tipmatrestado == 1) # Descomentar si deseas filtrar por estado activo
                .order_by(TipoMatricula.tipmatrid)
                .all())

        # Convertir los resultados en una lista de diccionarios con fechas formateadas
        response_data = [
            {
                "tipmatrid": row.tipmatrid,
                "tipmatrgestion": row.tipmatrgestion,
                "tipmatrfecini": row.tipmatrfecini.isoformat() if row.tipmatrfecini else None,
                "tipmatrfecfin": row.tipmatrfecfin.isoformat() if row.tipmatrfecfin else None,
                "tipmatrcosto": row.tipmatrcosto,
                "tipmatrusureg": row.tipmatrusureg,
                "tipmatrfecreg": row.tipmatrfecreg.isoformat() if row.tipmatrfecreg else None,
                "tipmatrusumod": row.tipmatrusumod,
                "tipmatrfecmod": row.tipmatrfecmod.isoformat() if row.tipmatrfecmod else None,
                "tipmatrestado": row.tipmatrestado,
                "tipmatrdescripcion": row.tipmatrdescripcion
            } for row in query
        ]

        # Crear la respuesta con los datos obtenidos
        return make_response(jsonify({
            "message": "Tipos de matrícula obtenidos con éxito",
            "data": response_data,
            "code": HTTPStatus.OK
        }), HTTPStatus.OK)

    except SQLAlchemyError as e:
        # Manejar cualquier error de SQLAlchemy
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()


def listarTipoMatriculaCombo():
    lista = select(f'''
        SELECT tipmatrid, tipmatrgestion
        FROM academico.tipo_matricula
        WHERE tipmatrestado = 1
        ORDER BY tipmatrgestion;
        ''')
    return lista

def listarTipoPersonaEstudiante():
    return select(f'''          
        select u.perid, p.pernomcompleto, p.perfoto 
        from academico.usuario u
        left join academico.persona p on p.perid = u.perid 
        where u.rolid = 4
        and p.perestado = 1
        and u.usuestado = 1
        order by p.pernomcompleto;
    ''')
















# otras funciones 

def eliminarMatricula(data):
    return execute_function(f'''
    SELECT academico.eliminar_matricula(
        \'{data['matrid']}\')  as valor;                      
    ''')  



def insertarTipoMatricula(data):
    return execute_function(f'''
    SELECT academico.f_tipo_matricula_insertar(
        \'{data['tipmatrgestion']}\',
        \'{data['tipmatrfecini']}\',
        \'{data['tipmatrfecfin']}\',
        {data['tipmatrcosto']},
        \'{data['tipmatrusureg']}\',
        \'{data['tipmatrdescripcion']}\')  as valor;
    ''')
    
def modificarTipoMatricula(data):
    return execute_function(f'''
    SELECT academico.f_tipo_matricula_modificar(
        {data['tipmatrid']},
        \'{data['tipmatrgestion']}\',
        \'{data['tipmatrfecini']}\',
        \'{data['tipmatrfecfin']}\',
        {data['tipmatrcosto']},
        \'{data['tipmatrusumod']}\',
        \'{data['tipmatrdescripcion']}\')  as valor;
    ''')    
    
def gestionarTipoMatriculaEstado(data):
    return execute_function(f'''
    SELECT academico.f_tipo_matricula_gestionar_estado(
        {data['tipo']},
        {data['tipmatrid']},
        \'{data['tipmatrusumod']}\')  as valor;
    ''')