from core.database import select, execute, execute_function, execute_response
from core.rml.report_generator import Report
from flask import make_response
from utils.date_formatting import *
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from core.database import db
from sqlalchemy.sql import func
from models.pago_model import Pago
from models.persona_model import Persona
from models.curso_materia_model import CursoMateria
from models.inscripcion_model import Inscripcion
from models.materia_model import Materia
from models.curso_model import Curso
from flask import jsonify, make_response
from http import HTTPStatus
from models.nota_model import Nota
def make(pdf):
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format("archivo.pdf")
    response.mimetype = 'application/pdf'
    return response

def gestionarNota(data):
    data = {key: f'\'{value}\'' if value is not None else 'NULL' for key, value in data.items()}

    return execute_function(f'''
       SELECT academico.f_gestionar_nota
                ({data['tipo']},
                {data['notid']}, 
                {data['insid']}, 
                {data['not1']}, 
                {data['not2']}, 
                {data['not3']},
                {data['notfinal']},
                {data['notusureg']}, 
                {data['notusumod']}, 
                {data['notestado']}) as valor;
    ''')

def listarNota():
    return select('''
        SELECT notid, insid, not1, not2, not3, notfinal, notusureg, notfecreg, notusumod, notfecmod, notestado FROM academico.nota;
    ''')
 
def listarNotaEstudiante(data):
    lista_nota_estudiante = select(f'''
        select distinct i.insid, i.matrid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid,  cm.periddocente, p.pernomcompleto, m.matnombre, i.peridestudiante, i.pagid, i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion 
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid
        left join academico.materia m on m.matid = cm.matid
         left join academico.persona p on p.perid = cm.periddocente
        where i.peridestudiante = {data['perid']}
    ''')
    for nota_estudiante in lista_nota_estudiante:
        nota_estudiante["insfecreg"] = darFormatoFechaConHora(nota_estudiante["insfecreg"])
        nota_estudiante["insfecmod"] = darFormatoFechaConHora(nota_estudiante["insfecmod"])
        nota_estudiante["curmatfecini"] = darFormatoFechaSinHora(nota_estudiante["curmatfecini"])
        nota_estudiante["curmatfecfin"] = darFormatoFechaSinHora(nota_estudiante["curmatfecfin"])   
    return lista_nota_estudiante

def listarNotaDocente(data):
    lista_nota_docente = select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin , cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        where cm.periddocente = {data['perid']}
        order by c.curnombre, m.matnombre; 
    ''')
    for nota_docente in lista_nota_docente:
        nota_docente["curmatfecreg"] = darFormatoFechaConHora(nota_docente["curmatfecreg"])
        nota_docente["curmatfecmod"] = darFormatoFechaConHora(nota_docente["curmatfecmod"])
        nota_docente["curmatfecini"] = darFormatoFechaSinHora(nota_docente["curmatfecini"])
        nota_docente["curmatfecfin"] = darFormatoFechaSinHora(nota_docente["curmatfecfin"])   
    
    return lista_nota_docente
    
def listarNotaEstudianteMateria(data):
    return select(f'''
        SELECT n.notid, n.insid, n.not1, n.not2, n.not3,
               n.notfinal, 
               i.peridestudiante,
               p.pernomcompleto,
               cm.matid, m.matnombre,
               cm.curid, c.curnombre,
               n.notusureg, n.notfecreg, n.notusumod, n.notfecmod, n.notestado 
        FROM academico.nota n
        left join academico.inscripcion i on i.insid = n.insid
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid
        left join academico.materia m on m.matid = cm.matid
        where i.peridestudiante = {data['perid']}
        and cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
        order by c.curnombre, m.matnombre; 
    ''')       
"""
def listarNotaEstudianteCurso(data):
    return select(f'''
        SELECT i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto, p.pernrodoc, p.perfoto, n.notid, n.not1, n.not2, n.not3, n.notfinal, n.notusureg, n.notfecreg, n.notusumod, n.notfecmod
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.nota n on n.insid = i.insid
        where i.curmatid = {data['curmatid']}
        order by p.pernomcompleto;
    ''')  
"""
def listarNotaEstudianteCurso(data):
    try:
        curmatid = data.get('curmatid')

        # Crear alias para las tablas si es necesario
        i = aliased(Inscripcion)
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        n = aliased(Nota)

        # Ejecutar la consulta
        query = (db.session.query(
                    i.insid,
                    c.curnombre,
                    m.matnombre,
                    i.peridestudiante,
                    p.pernomcompleto,
                    p.pernrodoc,
                    p.perfoto,
                    n.notid,
                    n.not1,
                    n.not2,
                    n.not3,
                    n.notfinal,
                    n.notusureg,
                    n.notfecreg,
                    n.notusumod,
                    n.notfecmod
                )
                .select_from(i)
                .join(cm, cm.curmatid == i.curmatid)
                .join(c, c.curid == cm.curid)
                .join(m, m.matid == cm.matid)
                .join(p, p.perid == i.peridestudiante)
                .outerjoin(n, n.insid == i.insid)
                .filter(i.curmatid == curmatid)
                .order_by(p.pernomcompleto)
                .all())
        
        # Convertir resultados a formato JSON
        lista_nota_estudiante_curso = [
            {
                'insid': row.insid,
                'curnombre': row.curnombre,
                'matnombre': row.matnombre,
                'peridestudiante': row.peridestudiante,
                'pernomcompleto': row.pernomcompleto,
                'pernrodoc': row.pernrodoc,
                'perfoto': row.perfoto,
                'notid': row.notid,
                'not1': row.not1,
                'not2': row.not2,
                'not3': row.not3,
                'notfinal': row.notfinal,
                'notusureg': row.notusureg,
                'notfecreg': row.notfecreg.isoformat() if row.notfecreg else None,
                'notusumod': row.notusumod,
                'notfecmod': row.notfecmod.isoformat() if row.notfecmod else None
            } for row in query
        ]

        return make_response(jsonify(lista_nota_estudiante_curso), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

def rptNotaEstudianteMateria(data):
    params = select(f'''
        SELECT n.notid, n.insid, n.not1, n.not2, n.not3,
               n.notfinal, 
               i.peridestudiante,
               p.pernomcompleto, p.pernrodoc, p.peremail, p.percelular, p.perfoto,
               cm.matid, m.matnombre,
               cm.curid, c.curnombre,
               n.notusureg, n.notfecreg, n.notusumod, n.notfecmod, n.notestado 
        FROM academico.nota n
        left join academico.inscripcion i on i.insid = n.insid
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid
        left join academico.materia m on m.matid = cm.matid
        where i.peridestudiante = {data['perid']}
        order by c.curnombre, m.matnombre
    ''')
    return make(Report().RptNotaEstudianteMateria(params, data['usuname']))


def rptNotaCursoMateria(data):
    params = select(f'''
        SELECT 
        i.insid, 
        c.curnombre,
        cm.periddocente, 
        p2.pernomcompleto as pernomcompletodocente, 
        p2.pernrodoc as pernrodocdocente,
        m.matnombre, 
        i.peridestudiante, 
        p.pernomcompleto, 
        p.perapepat,
        p.perapemat,
        p.pernombres,
        p.pernrodoc,
        p.perfoto, 
        n.notid, 
        n.not1, 
        n.not2, 
        n.not3, 
        n.notfinal, 
        n.notusureg, 
        n.notfecreg, 
        n.notusumod, 
        n.notfecmod,
        CASE
                WHEN n.notfinal >= 70 THEN 'Aprobado'
                ELSE 'Reprobado'
        END AS estado
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.persona p2 on p2.perid = cm.periddocente
        left join academico.nota n on n.insid = i.insid
        where i.curmatid = {data['curmatid']}
        order by p.pernomcompleto;
    ''')
    return make(Report().RptNotaCursoMateria(params, data['usuname']))

def rptNotaCursoMateriaGeneral(data):
    params = select(f'''
        SELECT
            i.insid,
            c.curnombre,
            m.matnombre,
            i.peridestudiante,
            p.pernomcompleto,
            p.perapepat,
            p.perapemat,
            p.pernombres,
            p.pernrodoc,
            p.perfoto,
            n.notid,
            n.not1,
            n.not2,
            n.not3,
            n.notfinal,
            n.notusureg,
            n.notfecreg,
            n.notusumod,
            n.notfecmod,
            CASE
                WHEN n.notfinal IS NULL THEN 'Pendiente'
                WHEN n.notfinal >= 70 THEN 'Aprobado'
                ELSE 'Reprobado'
            END AS estado
        FROM
            academico.inscripcion i
            LEFT JOIN academico.curso_materia cm ON cm.curmatid = i.curmatid
            LEFT JOIN academico.curso c ON c.curid = cm.curid 
            LEFT JOIN academico.materia m ON m.matid = cm.matid 
            LEFT JOIN academico.persona p ON p.perid = i.peridestudiante
            LEFT JOIN academico.nota n ON n.insid = i.insid
        ORDER BY
            c.curnombre,
            m.matnombre,
            p.pernomcompleto;            
    ''')
    return make(Report().RptNotaCursoMateriaGeneral(params, data['usuname']))


def rptNotaCursoMateriaDocente(data):
    params = select(f'''
        SELECT
            i.insid,
            c.curnombre,
            cm.periddocente, 
            p2.pernomcompleto as pernomcompletodocente, 
            p2.pernrodoc as pernrodocdocente,
            m.matnombre,
            i.peridestudiante,
            p.pernomcompleto,
            p.perapepat,
            p.perapemat,
            p.pernombres,
            p.pernrodoc,
            p.perfoto,
            n.notid,
            n.not1,
            n.not2,
            n.not3,
            n.notfinal,
            n.notusureg,
            n.notfecreg,
            n.notusumod,
            n.notfecmod,
            CASE
                WHEN n.notfinal >= 70 THEN 'Aprobado'
                ELSE 'Reprobado'
            END AS estado
        FROM
            academico.inscripcion i
            LEFT JOIN academico.curso_materia cm ON cm.curmatid = i.curmatid
            LEFT JOIN academico.curso c ON c.curid = cm.curid 
            LEFT JOIN academico.materia m ON m.matid = cm.matid 
            LEFT JOIN academico.persona p ON p.perid = i.peridestudiante
             left join academico.persona p2 on p2.perid = cm.periddocente
            LEFT JOIN academico.nota n ON n.insid = i.insid
        where cm.periddocente = {data['periddocente']}
        ORDER BY
            c.curnombre,
            m.matnombre,
            p.pernomcompleto;
    ''')
    return make(Report().RptNotaCursoMateriaDocente(params, data['usuname']))
    
"""  
def listarNotaCurso():
    lista = select(f'''
        SELECT distinct cm.curmatid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, p.perfoto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion, cm.curmatestado 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        --where cm.curmatestado = 1
        order by c.curnombre, m.matnombre;
    ''')  
    for pago in lista:
        # pago["curmatfecreg"] = darFormatoFechaConHora(pago["curmatfecreg"])
        # pago["curmatfecmod"] = darFormatoFechaConHora(pago["curmatfecmod"])
        pago["curmatfecini"] = darFormatoFechaSinHorav2(pago["curmatfecini"])
        pago["curmatfecfin"] = darFormatoFechaSinHorav2(pago["curmatfecfin"]) 
    return lista
"""

def listarNotaCurso():
    try:
        # Definir alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)  # Alias para la tabla de inscripciones
        
        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    cm.curmatid,
                    cm.curid,
                    cm.curmatfecini,
                    cm.curmatfecfin,
                    cm.matid,
                    cm.curmatusureg,
                    cm.curmatfecreg,
                    cm.curmatusumod,
                    cm.curmatfecmod,
                    cm.curmatestadodescripcion,
                    cm.curmatdescripcion,
                    cm.periddocente,
                    cm.curmatestado,
                    c.curnombre,
                    m.matnombre,
                    p.pernomcompleto,
                    p.perfoto,
                    p.pernrodoc,
                    func.count(i.insid).label('num_estudiantes')  # Contar el número de estudiantes
                )
                .outerjoin(c, c.curid == cm.curid)
                .outerjoin(m, m.matid == cm.matid)
                .outerjoin(p, p.perid == cm.periddocente)
                .outerjoin(i, i.curmatid == cm.curmatid)  # Unir con la tabla de inscripciones
                .group_by(cm.curmatid, c.curid, m.matid, p.perid)  # Agrupar por ID único de la combinación
                .order_by(c.curnombre, m.matnombre)
                .all())

        # Convertir los resultados en una lista de diccionarios
        lista = [
            {
                'curmatid': row.curmatid,
                'curid': row.curid,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'matid': row.matid,
                'curmatusureg': row.curmatusureg,
                'curmatfecreg': row.curmatfecreg.isoformat() if row.curmatfecreg else None,
                'curmatusumod': row.curmatusumod,
                'curmatfecmod': row.curmatfecmod.isoformat() if row.curmatfecmod else None,
                'curmatestadodescripcion': row.curmatestadodescripcion,
                'curmatdescripcion': row.curmatdescripcion,
                'curmatestado': row.curmatestado,
                'periddocente': row.periddocente,
                'curnombre': row.curnombre,
                'matnombre': row.matnombre,
                'pernomcompleto': row.pernomcompleto,
                'perfoto': row.perfoto,
                'pernrodoc': row.pernrodoc,
                'num_estudiantes': row.num_estudiantes  # Número de estudiantes
            } for row in query
        ]

        return make_response(jsonify(lista), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

def manage_nota(data):
    tipo = data.get('tipo')
    notid = data.get('notid')

    if tipo == 1:  # Crear nota
        return create_nota(data)
    elif tipo == 2:  # Actualizar nota
        if notid is not None:
            return update_nota(data, notid)
        else:
            return {"status": "error", "message": "Nota ID is required for update."}, HTTPStatus.BAD_REQUEST
    elif tipo == 3:  # Eliminar nota
        if notid is not None:
            return delete_nota(notid)
        else:
            return {"status": "error", "message": "Nota ID is required for delete."}, HTTPStatus.BAD_REQUEST
    else:
        return {"status": "error", "message": "Tipo de operación no soportada."}, HTTPStatus.BAD_REQUEST


def create_nota(data):
    try:
        nota = Nota(
            insid=data.get("insid"),
            not1=data.get("not1"),
            not2=data.get("not2"),
            not3=data.get("not3"),
            notfinal=data.get("notfinal"),
            notusureg=data.get("notusureg"),
            notusumod=data.get("notusureg"),
            notfecmod=datetime.now(),
            notfecreg=datetime.now(),
            notestado=data.get("notestado")
        )
        db.session.add(nota)
        db.session.commit()
        _data = nota.to_dict()
        response_data = {
            "message": "Nota created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        return make_response(jsonify(response_data), HTTPStatus.CREATED)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
from decimal import Decimal    
from models.nota_model import Nota, db
def update_nota(data, notid):
    try:
        nota = Nota.query.filter_by(notid=notid).first()
        if not nota:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)         
    
        nota.insid = data.get("insid", nota.insid)
        nota.not1 = Decimal(data.get("not1", nota.not1))
        nota.not2 = Decimal(data.get("not2", nota.not2))
        nota.not3 = Decimal(data.get("not3", nota.not3))
        nota.notfinal = data.get("notfinal", nota.notfinal)
        nota.notusumod = data.get("notusumod", nota.notusumod)
        nota.notfecmod = datetime.now()
        nota.notestado = data.get("notestado", nota.notestado)

        db.session.commit()
        _data = nota.to_dict()
        response_data = {
            "message": "Nota updated successfully",
            "data": _data,
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


def delete_nota(notid):
    try:
        nota = Nota.query.filter_by(notid=notid).first()
        if not nota:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(nota)
        db.session.commit()

        response_data = {
            "message": "Nota deleted successfully",
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
