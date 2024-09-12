from http import HTTPStatus

from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from utils.date_formatting import *
from sqlalchemy.exc import SQLAlchemyError  # Importa las excepciones de SQLAlchemy

# Importar los modelos
from models.curso_materia_model import CursoMateria, db
from models.curso_model import Curso
from models.persona_model import Persona
from models.usuario_model import Usuario
from models.rol_model import Rol
def getListCursoMateria():
    try:
        # Definir alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        u = aliased(Usuario)
        r = aliased(Rol)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    cm.curmatid, cm.curmatfecini, cm.curmatfecfin, cm.matid, cm.periddocente, 
                    cm.curmatidrol.label('rolid'), cm.curmatidroldes.label('rolnombre'), cm.curmatcosto,
                    c.curid, c.curnombre, c.curfchini, c.curfchfin, c.curnivel,
                    m.matnombre, m.matnivel, 
                    p.pernomcompleto, p.pernrodoc, p.perfoto, p.pernombres, p.perapemat, p.perapepat, 
                    cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestado
                )
                .distinct()
                .outerjoin(cm, cm.curid == c.curid)
                .outerjoin(m, m.matid == cm.matid)
                .outerjoin(p, p.perid == cm.periddocente)
                .outerjoin(u, u.perid == cm.periddocente)
                .outerjoin(r, r.rolid == u.rolid)
                .all())
                

        # Convertir los resultados en una lista de diccionarios
        list_curso_materia = [
            {
                'curmatid': row.curmatid,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'matid': row.matid,
                'periddocente': row.periddocente,
                'rolid': row.rolid,
                'rolnombre': row.rolnombre,
                'curmatcosto': row.curmatcosto,
                'curid': row.curid,
                'curnombre': row.curnombre,
                'curfchini': row.curfchini.isoformat() if row.curfchini else None,
                'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,
                'curnivel': row.curnivel,
                'matnombre': row.matnombre,
                'matnivel': row.matnivel,
                'pernomcompleto': row.pernomcompleto,
                'pernrodoc': row.pernrodoc,
                'perfoto': row.perfoto,
                'pernombres': row.pernombres,
                'perapemat': row.perapemat,
                'perapepat': row.perapepat,
                'curmatusureg': row.curmatusureg,
                'curmatfecreg': row.curmatfecreg.isoformat() if row.curmatfecreg else None,
                'curmatusumod': row.curmatusumod,
                'curmatfecmod': row.curmatfecmod.isoformat() if row.curmatfecmod else None,
                'curmatestado': row.curmatestado
            } for row in query
        ]

        return make_response(jsonify(list_curso_materia), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()
    
def eliminarCursoMateria(data):
    resultado = execute_function(f'''
    SELECT academico.eliminar_curso_materia({data['curmatid']}) as valor;
    ''')
    result = resultado[0]['valor']
    if result == 1:
        response_data = {'message': 'Curso Materia eliminado correctamente'}
        status_code = 200
    else:
        if result == 0:
            response_data = {'message': 'No se pudo eliminar el curso materia'}
            status_code = 500
        else:
            response_data = {'message': 'No se puede eliminar la curso materia debido a que tiene registros relacionados'}
            status_code = 500
    return make_response(jsonify(response_data), status_code)

def insertarCursoMateria(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL(''' SELECT academico.insertar_curso_materia ({curid}, {matid}, {perid}, {fecini}, {fecfin}, {estado}, {estadodes}, {usureg}, {idrol}, {idroldes}, {costo});''').format( curid = sql.Literal(data['curid']), matid = sql.Literal(data['matid']), perid = sql.Literal(data['periddocente']), fecini = sql.Literal(data['curmatfecini']), fecfin = sql.Literal(data['curmatfecfin']), estado = sql.Literal(data['curmatestado']), estadodes = sql.Literal(data['curmatestadodescripcion']), usureg = sql.Literal(data['curmatusureg']), idrol = sql.Literal(data['curmatidrol']), idroldes = sql.Literal(data['curmatidroldes']), costo = sql.Literal(data['curmatcosto']) )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def modificarCursoMateria(data):
    resultado = execute_function(f'''
        SELECT academico.modificar_curso_materia(
              {data['curmatid']},
              {data['curid']},
              {data['matid']},
              {data['periddocente']},
            \'{data['curmatfecini']}\',
            \'{data['curmatfecfin']}\',
              {data['curmatestado']},
            \'{data['curmatestadodescripcion']}\',
            \'{data['curmatusumod']}\',
            \'{data['curmatidrol']}\',
            \'{data['curmatidroldes']}\',
              {data['curmatcosto']}
        ) as valor;
         ''')
    return resultado

def listaCursoCombo():
    return select(f'''
    SELECT curid, curnombre, curnivel
    FROM academico.curso
    where curestado = 1
    order by curnivel      
    ''')

def listaPersonaDocenteCombo(data):
    return select(f'''
    select distinct p.perid, p.pernomcompleto, p.perfoto, p.pernrodoc
    from academico.persona p 
    inner join academico.usuario u on u.perid = p.perid
    inner join academico.rol r ON r.rolid = u.rolid
    where r.rolnombre = \'{data['rolnombre']}\'
    and p.perestado = 1
    order by p.pernomcompleto  
    ''')
    
def tipoRol():
    return select(f'''
    SELECT rolid, rolnombre
	FROM academico.rol
	order by rolnombre;                
    ''')
    
def gestionarCursoMateriaEstado(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
                        SELECT academico.f_curso_materia_gestionar_estado
                        ({tipo}, {curmatid}, {curmatusumod});''').format(
                            tipo = sql.Literal(data['tipo']),
                            curmatid = sql.Literal(data['curmatid']),
                            curmatusumod = sql.Literal(data['curmatusumod'])
                        )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def getCursoById(curid):
    try:
        # Buscar el curso por ID
        curso = Curso.query.get(curid)
        
        # Si no se encuentra el curso, devolver un error 404
        if curso is None:
            return make_response(jsonify({"error": "Curso no encontrado"}), HTTPStatus.NOT_FOUND)
        
        # Convertir el objeto `Curso` a un diccionario
        curso_data = curso.to_dict()
        
        # Crear la respuesta con el objeto `Curso`
        response_data = {
            "message": "Curso obtenido con éxito",
            "data": curso_data,
            "code": HTTPStatus.OK
        }
        
        return make_response(jsonify(response_data), HTTPStatus.OK)
    
    except Exception as e:
        # Manejar cualquier error inesperado
        error_response = {
            "error": "Error en la base de datos",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def getTipoCurso():
    try:
        # Obtener los tipos de cursos de la base de datos
        tipos_cursos = Curso.query.order_by(Curso.curnombre).all()
        # Convertir los tipos de cursos en una lista de diccionarios
        response = [{"curid": tipo.curid, "curnombre": tipo.curnombre} for tipo in tipos_cursos]
        # Retornar los tipos de cursos como una respuesta JSON
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        # En caso de error, devolver un mensaje de error con el código de estado correspondiente
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.curso_materia_model import CursoMateria
from models.materia_model import Materia, db
from sqlalchemy.orm import aliased

def getTipoMateriaByCursoId(curid):
    """
    Obtiene la lista de materias asociadas a un curso específico.

    Esta función realiza una consulta a la base de datos para obtener todas las materias 
    vinculadas a un curso específico utilizando un `LEFT JOIN`. Solo se seleccionan aquellas 
    materias cuyo estado en `CursoMateria` es 1.

    Args:
        curid (int): El ID del curso para el cual se desean obtener las materias.

    Returns:
        Response: Una respuesta JSON con un mensaje de éxito y los datos de las materias, o un 
        mensaje de error si ocurre una excepción.
    """
    try:
        # Definir alias para las tablas
        cm = aliased(CursoMateria)
        m = aliased(Materia)
        
        # Realizar la consulta con left join y filtrado por curmatestado = 1
        query = (db.session.query(
                    cm.matid,
                    m.matnombre,
                    cm.curmatfecini,
                    cm.curmatfecfin
                )
                .outerjoin(m, cm.matid == m.matid)
                .filter(cm.curid == curid, cm.curmatestado == 1)
                .all())
        
        # Convertir los resultados en una lista de diccionarios con fechas formateadas
        response_data = [
            {
                "matid": row.matid,
                "matnombre": row.matnombre,
                "curmatfecini": row.curmatfecini.isoformat() if row.curmatfecini else None,
                "curmatfecfin": row.curmatfecfin.isoformat() if row.curmatfecfin else None
            } for row in query
        ]

        # Crear la respuesta con los datos obtenidos
        return make_response(jsonify({
            "message": "Materias obtenidas con éxito",
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
