from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from sqlalchemy import func, distinct
from utils.date_formatting import *
from sqlalchemy.orm import joinedload
from datetime import datetime
from models.inscripcion_model import Inscripcion, db 
from models.matricula_model import Matricula
from models.persona_model import Persona 
from models.pago_model import Pago 
from models.curso_materia_model import CursoMateria
from models.curso_model import Curso
from models.materia_model import Materia
from models.tipo_matricula_model import TipoMatricula
# Realizamos una consulta a la base de datos usando SQLAlchemy ORM
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, make_response
from http import HTTPStatus

def listarInscripcion():
    """
    Lista todas las inscripciones con los detalles relacionados de las tablas asociadas.

    Esta función realiza una consulta a la base de datos para obtener todas las inscripciones
    junto con los detalles de las tablas relacionadas como `Matricula`, `Persona`, `Pago`, `CursoMateria`, `Curso`,
    `Materia` y `TipoMatricula`.

    Returns:
        Response: Una respuesta JSON con un mensaje de éxito y los datos de las inscripciones, o un 
        mensaje de error si ocurre una excepción.
    """
    try:
        # Definir alias para las tablas
        Estudiante = aliased(Persona)
        Docente = aliased(Persona)
        
        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    Inscripcion.insid,
                    Inscripcion.matrid,
                    Inscripcion.pagid,
                    Inscripcion.curmatid,
                    Matricula.tipmatrid,
                    Matricula.matrestado,
                    Matricula.matrdescripcion,
                    TipoMatricula.tipmatrgestion,
                    Inscripcion.peridestudiante,
                    Estudiante.pernomcompleto.label('pernombrecompletoestudiante'),
                    Estudiante.perfoto.label('perfotoestudiante'),
                    Estudiante.pernrodoc.label('pernrodocestudiante'),
                    Pago.pagdescripcion,
                    Pago.pagtipo,
                    Pago.pagmonto,
                    Pago.pagfecha,
                    Pago.pagarchivo,
                    CursoMateria.curid,
                    CursoMateria.matid,
                    CursoMateria.curmatdescripcion,
                    CursoMateria.curmatfecini,
                    CursoMateria.curmatfecfin,
                    CursoMateria.periddocente,
                    Curso.curnombre,
                    Curso.curnivel,
                    Materia.matnombre,
                    Docente.pernomcompleto.label('pernombrecompletodocente'),
                    Docente.perfoto.label('perfotodocente'),
                    Docente.pernrodoc.label('pernrodocdocente'),
                    Inscripcion.insusureg,
                    Inscripcion.insfecreg,
                    Inscripcion.insusumod,
                    Inscripcion.insfecmod,
                    Inscripcion.insestado,
                    Inscripcion.insestadodescripcion
                )
                .join(Matricula, Inscripcion.matrid == Matricula.matrid)
                .join(Estudiante, Inscripcion.peridestudiante == Estudiante.perid)
                .outerjoin(Pago, Inscripcion.pagid == Pago.pagid)
                .join(CursoMateria, Inscripcion.curmatid == CursoMateria.curmatid)
                .join(Curso, CursoMateria.curid == Curso.curid)
                .join(Materia, CursoMateria.matid == Materia.matid)
                .join(Docente, CursoMateria.periddocente == Docente.perid)
                .join(TipoMatricula, Matricula.tipmatrid == TipoMatricula.tipmatrid)
                .order_by(Inscripcion.insid.desc())
                .all())

        # Convertir los resultados en una lista de diccionarios con fechas formateadas
        response_data = [
            {
                "insid": row.insid,
                "matrid": row.matrid,
                "pagid": row.pagid,
                "curmatid": row.curmatid,
                "tipmatrid": row.tipmatrid,
                "matrestado": row.matrestado,
                "matrdescripcion": row.matrdescripcion,
                "tipmatrgestion": row.tipmatrgestion,
                "peridestudiante": row.peridestudiante,
                "pernombrecompletoestudiante": row.pernombrecompletoestudiante,
                "perfotoestudiante": row.perfotoestudiante,
                "pernrodocestudiante": row.pernrodocestudiante,
                "pagdescripcion": row.pagdescripcion,
                "pagtipo": row.pagtipo,
                "pagmonto": row.pagmonto,
                "pagfecha": row.pagfecha.isoformat() if row.pagfecha else None,
                "pagarchivo": row.pagarchivo,
                "curid": row.curid,
                "matid": row.matid,
                "curmatdescripcion": row.curmatdescripcion,
                "curmatfecini": row.curmatfecini.isoformat() if row.curmatfecini else None,
                "curmatfecfin": row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                "periddocente": row.periddocente,
                "curnombre": row.curnombre,
                "curnivel": row.curnivel,
                "matnombre": row.matnombre,
                "pernombrecompletodocente": row.pernombrecompletodocente,
                "perfotodocente": row.perfotodocente,
                "pernrodocdocente": row.pernrodocdocente,
                "insusureg": row.insusureg,
                "insfecreg": row.insfecreg.isoformat() if row.insfecreg else None,
                "insusumod": row.insusumod,
                "insfecmod": row.insfecmod.isoformat() if row.insfecmod else None,
                "insestado": row.insestado,
                "insestadodescripcion": row.insestadodescripcion
            } for row in query
        ]

        # Crear la respuesta con los datos obtenidos
        return make_response(jsonify({
            "message": "Inscripciones obtenidas con éxito",
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


"""
def listarInscripcion():
    lista_inscripciones = select(f'''
        SELECT 
        distinct
        i.insid, 
        i.matrid, m.tipmatrid, tm.tipmatrgestion, m.matrestado, m.matrdescripcion,   
        i.peridestudiante, p.pernomcompleto as pernombrecompletoestudiante, p.perfoto, 
        i.pagid, p2.pagdescripcion,  p2.pagtipo, p2.pagmonto, p2.pagfecha, p2.pagarchivo,
        i.curmatid, cm.curid, cm.curmatdescripcion, c.curnombre, cm.matid, 
        cm.curmatfecini, cm.curmatfecfin,
        m2.matnombre,
        cm.periddocente, p3.pernomcompleto as pernombrecompletodocente, p3.perfoto as perfotodocente,
        i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, 
        i.insestado, i.insestadodescripcion
        FROM academico.inscripcion i
        left join academico.matricula m on i.matrid = m.matrid
        left join academico.persona p on i.peridestudiante = p.perid 
        left join academico.pago p2 on i.pagid = p2.pagid
        left join academico.curso_materia cm on i.curmatid = cm.curmatid   
        left join academico.curso c on cm.curid = c.curid
        left join academico.materia m2 on cm.matid = m2.matid
        left join academico.persona p3 on cm.periddocente = p3.perid
        left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
        order by i.insid desc;
    ''')
    for curso in lista_inscripciones:
        curso["insfecreg"] = darFormatoFechaConHora(curso["insfecreg"])
        curso["insfecmod"] = darFormatoFechaConHora(curso["insfecmod"])
        curso["curmatfecini"] = darFormatoFechaSinHora(curso["curmatfecini"])
        curso["curmatfecfin"] = darFormatoFechaSinHora(curso["curmatfecfin"])
    return lista_inscripciones
""" 

def listarComboCursoMateria():
    lista_comboCursoMateria = select('''
        SELECT DISTINCT  
            cm.curmatid,
            c.curnombre,
            m.matnombre,
            cm.curmatfecini,
            cm.curmatfecfin
        FROM academico.curso_materia cm
        LEFT JOIN academico.curso c ON c.curid = cm.curid 
        LEFT JOIN academico.materia m ON m.matid = cm.matid;
    ''')

    resultado = []

    for cursoCombo in lista_comboCursoMateria:
        curmatdescripcion = f'{cursoCombo["curnombre"]} - {cursoCombo["matnombre"]} - { darFormatoFechaSinHora(cursoCombo["curmatfecini"])} a { darFormatoFechaSinHora(cursoCombo["curmatfecfin"])}'
        resultado.append({"curmatid": cursoCombo["curmatid"], "curmatdescripcion": curmatdescripcion})

    resultado.sort(key=lambda x: x["curmatdescripcion"])
    return resultado

def listarComboMatriculaEstudiante(data):
    return select(f'''
    select m.matrid, m.tipmatrid, tm.tipmatrgestion, m.peridestudiante, p.pernomcompleto, p.perfoto
    from academico.matricula m
    left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
    left join academico.persona p on p.perid = m.peridestudiante
    where m.peridestudiante = {data['peridestudiante']}
    and m.matrestado = 1    
    order by tm.tipmatrgestion;
    ''')

def listarComboMatricula():
    return select(f'''
    SELECT matrid, matrgestion
    FROM academico.matricula
    WHERE matrestado = 1
    order by matrgestion desc;
    ''')
    
def obtenerCursoMateria(data):
    return select(f'''
    SELECT cm.curmatid
    FROM academico.curso_materia cm
    where cm.curid = {data['curid']} 
    and cm.matid = {data['matid']}
    ''')
    
def insertarInscripcion(data):
    if data['pagid'] is not None:
        pagid = data['pagid']
    else:
        pagid = 'null'

    return execute_function(f'''
    SELECT academico.insertar_inscripcion(
          {data['matrid']}, 
          {data['peridestudiante']}, 
          {pagid}, 
        \'{data['insusureg']}\',
          {data['curmatid']}, 
          {data['insestado']}, 
        \'{data['insestadodescripcion']}\')  as valor;                      
    ''')

def modificarInscripcion(data):
    if data['pagid'] is not None:
        pagid = data['pagid']
    else:
        pagid = 'null'
    return execute_function(f'''
    SELECT academico.modificar_inscripcion(
          {data['insid']}, 
          {data['matrid']}, 
          {data['peridestudiante']}, 
          {pagid}, 
        \'{data['insusumod']}\',
          {data['curmatid']}, 
          {data['insestado']}, 
        \'{data['insestadodescripcion']}\')  as valor;                      
    ''')  

def eliminarInscripcion(data):
    return execute_function(f'''
    SELECT academico.eliminar_inscripcion(
        {data['insid']})  as valor;                      
    ''') 
    
def gestionarInscripcionEstado(data):
    return execute_function(f'''
    SELECT academico.f_inscripcion_gestionar_estado(
          {data['tipo']},    
          {data['insid']},    
          \'{data['insusumod']}\'
    ) as valor;
    ''')

"""
def obtenerEstudiantesInscritos(data):
    return select(f'''
    select peridestudiante as perid 
    from academico. inscripcion i
    where curmatid = {data['curmatid']}
    and i.insestado = 1
    ''')
""" 
    
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask import jsonify, make_response
from http import HTTPStatus
from models.inscripcion_model import Inscripcion, db

def obtenerEstudiantesInscritos(data):
    curid  = data['curid']
    matid = data['matid']
    curmatfecini = data['curmatfecini']
    curmatfecfin = data['curmatfecfin']
    
    try:
        # Convertir las fechas de string a objetos datetime para asegurar la integridad de los datos
        curmatfecini = datetime.strptime(curmatfecini, '%Y-%m-%d')
        curmatfecfin = datetime.strptime(curmatfecfin, '%Y-%m-%d')

        I = aliased(Inscripcion)
        CM = aliased(CursoMateria)

        # Realizar la consulta utilizando SQLAlchemy ORM
        query = (
            db.session.query(
                I.peridestudiante, CM.curmatid
            )
            .join(CM, I.curmatid == CM.curmatid)
            .filter(
                CM.curid == curid,
                CM.matid == matid,
                CM.curmatfecini == curmatfecini,
                CM.curmatfecfin == curmatfecfin,
                I.insestado == 1
            )
        )

        # Ejecutar la consulta y obtener los resultados
        result = query.all()

        # Convertir los resultados a una lista de diccionarios
        response_data = [
            {                
                "peridestudiante": row.peridestudiante,
                "curmatid": row.curmatid
            }
            for row in result
        ]

        print("data:::: ", response_data)

        # Crear la respuesta con los datos obtenidos
        return make_response(jsonify({
            "message": "Estudiantes inscritos obtenidos con éxito",
            "data": response_data,
            "code": HTTPStatus.OK
        }), HTTPStatus.OK)

    except SQLAlchemyError as e:
        # Manejar cualquier error de SQLAlchemy
        error_response = {
            "error": "Error en la base de datos",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getCursoMateriaByIds(data):
    curid = data['curid']
    matid = data['matid']
    curmatfecini = data['curmatfecini']
    curmatfecfin = data['curmatfecfin']
    
    try:
        # Convertir las fechas de string a objetos datetime para asegurar la integridad de los datos
        curmatfecini = datetime.strptime(curmatfecini, '%Y-%m-%d')
        curmatfecfin = datetime.strptime(curmatfecfin, '%Y-%m-%d')

        CM = aliased(CursoMateria)

        # Realizar la consulta utilizando SQLAlchemy ORM
        query = (
            db.session.query(
                CM.curmatid
            )
            .filter(
                CM.curid == curid,
                CM.matid == matid,
                CM.curmatfecini == curmatfecini,
                CM.curmatfecfin == curmatfecfin
            )
        )

        # Ejecutar la consulta y obtener el resultado
        result = query.first()

        # Si no se encuentra ningún resultado, devolver un mensaje adecuado
        if result is None:
            return make_response(jsonify({
                "message": "No se encontró ningún curso materia con los parámetros proporcionados",
                "data": None,
                "code": HTTPStatus.NOT_FOUND
            }), HTTPStatus.NOT_FOUND)

        # Crear la respuesta con el curmatid obtenido
        return make_response(jsonify({
            "message": "curmatid obtenido con éxito",
            "curmatid": result.curmatid,
            "code": HTTPStatus.OK
        }), HTTPStatus.OK)

    except SQLAlchemyError as e:
        # Manejar cualquier error de SQLAlchemy
        error_response = {
            "error": "Error en la base de datos",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)