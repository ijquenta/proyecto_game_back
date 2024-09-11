# ------------- Librerías de Python -------------
import decimal
from decimal import Decimal
from http import HTTPStatus

# ------------- Librerías de Flask -------------
from flask import jsonify, make_response

# ------------- Módulos de la aplicación -------------
from core.database import select, execute, execute_function, execute_response
from core.database import db  # Asegúrate de importar `db` solo una vez
from core.rml.report_generator import Report
from utils.date_formatting import *

# ------------- Modelos -------------
from models.nota_model import Nota
from models.pago_model import Pago
from models.persona_model import Persona
from models.curso_materia_model import CursoMateria
from models.inscripcion_model import Inscripcion
from models.materia_model import Materia
from models.curso_model import Curso

# ------------- Librerías de SQLAlchemy -------------
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy import case


def make(pdf):
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(
        "archivo.pdf")
    response.mimetype = 'application/pdf'
    return response

def gestionarNota(data):
    data = {key: f'\'{value}\'' if value is not None else 'NULL' for key,
            value in data.items()}

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
        select distinct i.insid, i.matrid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, cm.curmatestado, c.curfchini, c.curfchfin,
        cm.periddocente, p.pernomcompleto, p.pernrodoc, p.perfoto, m.matnombre, i.peridestudiante, i.pagid, i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion,
        n.notfinal, n.notestado
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid
        left join academico.materia m on m.matid = cm.matid
        left join academico.persona p on p.perid = cm.periddocente
        left join academico.nota n on n.insid = i.insid
        where i.peridestudiante = {data['perid']}
    ''')
    for nota_estudiante in lista_nota_estudiante:
        nota_estudiante["insfecreg"] = darFormatoFechaConHora(
            nota_estudiante["insfecreg"])
        nota_estudiante["insfecmod"] = darFormatoFechaConHora(
            nota_estudiante["insfecmod"])
        nota_estudiante["curmatfecini"] = darFormatoFechaSinHora(
            nota_estudiante["curmatfecini"])
        nota_estudiante["curmatfecfin"] = darFormatoFechaSinHora(
            nota_estudiante["curmatfecfin"])
        nota_estudiante["curfchini"] = darFormatoFechaSinHora(
            nota_estudiante["curfchini"])
        nota_estudiante["curfchfin"] = darFormatoFechaSinHora(
            nota_estudiante["curfchfin"])
    return lista_nota_estudiante

def listarNotaDocente(data):
    try:
        # Obtener el ID del docente
        perid_docente = data.get('perid')

        # Crear alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)

        # Ejecutar la consulta
        query = (db.session.query(
            cm.curmatid,
            cm.curid,
            c.curnombre,
            c.curfchini,
            c.curfchfin,
            cm.curmatfecini,
            cm.curmatfecfin,
            cm.matid,
            m.matnombre,
            cm.periddocente,
            p.pernomcompleto,
            cm.curmatusureg,
            cm.curmatfecreg,
            cm.curmatusumod,
            cm.curmatfecmod,
            cm.curmatestadodescripcion,
            cm.curmatdescripcion,
            cm.curmatestado,
            # Contar el número de estudiantes
            func.count(i.insid).label('num_estudiantes')
        )
            .select_from(cm)
            .join(c, c.curid == cm.curid)
            .join(m, m.matid == cm.matid)
            .join(p, p.perid == cm.periddocente)
            # Unir con inscripciones para contar estudiantes
            .outerjoin(i, i.curmatid == cm.curmatid)
            .filter(cm.periddocente == perid_docente)
            .group_by(cm.curmatid, cm.curid, c.curnombre, c.curfchini, c.curfchfin, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, 
                      cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, cm.curmatdescripcion)
            .order_by(c.curnombre, m.matnombre)
            .all())

        # Formatear las fechas y convertir los resultados a formato JSON
        lista_nota_docente = [
            {
                'curmatid': row.curmatid,
                'curid': row.curid,
                'curfchini': row.curfchini.isoformat() if row.curfchini else None,
                'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,
                'curnombre': row.curnombre,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'matid': row.matid,
                'matnombre': row.matnombre,
                'periddocente': row.periddocente,
                'pernomcompleto': row.pernomcompleto,
                'curmatusureg': row.curmatusureg,
                'curmatfecreg': row.curmatfecreg.isoformat() if row.curmatfecreg else None,
                'curmatusumod': row.curmatusumod,
                'curmatfecmod': row.curmatfecmod.isoformat() if row.curmatfecmod else None,
                'curmatestadodescripcion': row.curmatestadodescripcion,
                'curmatdescripcion': row.curmatdescripcion,
                'num_estudiantes': row.num_estudiantes,  # Número de estudiantes inscritos
                'curmatestado': row.curmatestado,
            } for row in query
        ]

        return make_response(jsonify(lista_nota_docente), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

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
        query = (db.session.query(i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto, p.pernrodoc, p.perfoto, n.notid, n.not1, n.not2, n.not3, n.notfinal, n.notusureg, n.notfecreg, n.notusumod, n.notfecmod)
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
             'insid': row.insid, 'curnombre': row.curnombre, 'matnombre': row.matnombre, 'peridestudiante': row.peridestudiante, 'pernomcompleto': row.pernomcompleto, 'pernrodoc': row.pernrodoc, 'perfoto': row.perfoto, 'notid': row.notid, 'not1': row.not1, 'not2': row.not2, 'not3': row.not3, 'notfinal': row.notfinal, 'notusureg': row.notusureg, 'notfecreg': row.notfecreg.isoformat() if row.notfecreg else None, 'notusumod': row.notusumod, 'notfecmod': row.notfecmod.isoformat() if row.notfecmod else None
            } for row in query
        ]

        return make_response(jsonify(lista_nota_estudiante_curso), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

def rptNotaEstudianteMateria(data):
    try:
        # Definir los alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)    
        p = aliased(Persona)
        i = aliased(Inscripcion)
        n = aliased(Nota)
        p2 = aliased(Persona)

        # Definir la consulta
        query = (db.session.query(n.notid, n.insid, n.not1, n.not2, n.not3, n.notfinal,  i.peridestudiante, p.pernomcompleto, p.pernrodoc, p.peremail, p.percelular, p.perfoto, cm.matid, m.matnombre, cm.curmatfecini, cm.curmatfecfin, cm.curid, c.curnombre, c.curfchini, c.curfchfin, n.notusureg, n.notfecreg, n.notusumod, n.notfecmod, n.notestado, p2.pernomcompleto.label('pernomcompletodocente'), p2.pernrodoc.label('pernrodocdocente'))
        .join(i, i.insid == n.insid)  # Unir con la tabla Inscripción
        .join(p, p.perid == i.peridestudiante)  # Unir con la tabla Persona Estudiante
        .join(cm, cm.curmatid == i.curmatid)  # Unir con la tabla CursoMateria
        .join(c, c.curid == cm.curid)  # Unir con la tabla Curso
        .join(m, m.matid == cm.matid)  # Unir con la tabla Materia
        .join(p2, p2.perid == cm.periddocente)
        .filter(i.peridestudiante == data['perid'])  # Filtrar por perid Estudiante
        .order_by(c.curnombre, m.matnombre)  # Ordenar por curnombre y matnombre
        .all()
        )

        # Inicializar variables para estadísticas
        total_materias = 0
        materias_aprobadas = 0
        materias_reprobadas = 0
        materias_abandonadas = 0
        total_notas = 0.0
        total_notas_aprobadas = 0.0

        # Inicializar un diccionario para agrupar los cursos
        cursos_agrupados = {}

        # Inicializar el diccionario para la información del estudiante
        estudiante = {}

        # Iterar sobre los resultados de la consulta y agrupar por curnombre
        for row in query:
            # Generar la llave basada en curnombre y las fechas del curso-materia
            llave = row.curnombre + ' ' + row.curfchini.isoformat() + ' - ' + row.curfchfin.isoformat()

            # Obtener la nota final y asegurar que sea un float
            nota_final = float(row.notfinal) if isinstance(row.notfinal, decimal.Decimal) else row.notfinal

            # Actualizar conteos y totales
            total_materias += 1
            total_notas += nota_final

            if nota_final == 0:
                materias_abandonadas += 1
            elif nota_final > 70:
                materias_aprobadas += 1
                total_notas_aprobadas += nota_final
            else:
                materias_reprobadas += 1

            # Crear el objeto de la lista
            elemento = {
                'nota': { 'nottid': row.notid, 'not1': row.not1, 'not2': row.not2, 'not3': row.not3, 'notfinal': nota_final, 'notusureg': row.notusureg, 'notfecreg': row.notfecreg.isoformat() if row.notfecreg else None, 'notusumod': row.notusumod, 'notfecmod': row.notfecmod.isoformat() if row.notfecmod else None, 'notestado': row.notestado, 'notdescripcion': 'Abandono' if nota_final == 0 else 'Aprobado' if nota_final > 70 else 'Reprobado'},
                'curso_materia': { 'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None, 'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None, 'matid': row.matid, 'matnombre': row.matnombre, 'curid': row.curid, 'curnombre': row.curnombre, 'curfchini': row.curfchini.isoformat() if row.curfchini else None, 'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None },
                'docente': { 'pernomcompletodocente': row.pernomcompletodocente, 'pernrodocdocente': row.pernrodocdocente }
            }

            # Asignar la información del estudiante (solo una vez)
            if not estudiante:
                estudiante = { 'peridestudiante': row.peridestudiante, 'pernomcompleto': row.pernomcompleto, 'pernrodoc': row.pernrodoc, 'peremail': row.peremail, 'percelular': row.percelular, 'perfoto': row.perfoto
                }

            # Si la llave ya existe en el diccionario, agregamos el elemento a la lista
            if llave in cursos_agrupados:
                cursos_agrupados[llave].append(elemento)
            else:
                # Si la llave no existe, la creamos con una lista que contiene el elemento
                cursos_agrupados[llave] = [elemento]

        # Calcular el promedio general
        promedio_general = total_notas / total_materias if total_materias > 0 else 0
        promedio_general_rounded = round(promedio_general, 2)

        # Calcular el promedio de notas aprobadas
        promedio_aprobadas = total_notas_aprobadas / materias_aprobadas if materias_aprobadas > 0 else 0
        promedio_aprobadas_rounded = round(promedio_aprobadas, 2)

        # Preparar los datos de resumen
        resumen = { 'total_materias': total_materias, 'materias_aprobadas': materias_aprobadas, 'materias_reprobadas': materias_reprobadas, 'materias_abandonadas': materias_abandonadas, 'promedio_general': promedio_general_rounded, 'promedio_aprobadas': promedio_aprobadas_rounded}

        # Generar y devolver el reporte en PDF
        return make(Report().RptNotaEstudianteMateria(cursos_agrupados, estudiante, data['usuname'], resumen))

    except Exception as e:
        print(f"Error rpt NotaEstudianteMateria: {e}")
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

def rptNotaCursoMateria(data):
    try:
        # Definir los alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)    
        p = aliased(Persona)
        i = aliased(Inscripcion)
        n = aliased(Nota)
        p2 = aliased(Persona)  # Alias para el docente

        # Definir la consulta
        query = (
            db.session.query(
                i.insid,
                c.curnombre,
                c.curfchini,
                c.curfchfin,
                cm.periddocente,
                cm.curmatfecini,
                cm.curmatfecfin,
                p2.pernomcompleto.label('pernomcompletodocente'),
                p2.pernrodoc.label('pernrodocdocente'),
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
                case(
                    [(n.notfinal >= 70, 'Aprobado')],
                    else_='Reprobado'
                ).label('estado')
            )
            .join(cm, cm.curmatid == i.curmatid)  # Unir con la tabla CursoMateria (solo una vez)
            .join(c, c.curid == cm.curid)  # Unir con la tabla Curso
            .join(m, m.matid == cm.matid)  # Unir con la tabla Materia
            .join(p2, p2.perid == cm.periddocente)  # Unir con la tabla Persona Docente
            .join(p, p.perid == i.peridestudiante)  # Unir con la tabla Persona Estudiante
            .join(n, n.insid == i.insid)  # Unir con la tabla Nota
            .filter(i.curmatid == data['curmatid'])  # Filtrar por el curso-materia
            .order_by(p.pernomcompleto)  # Ordenar por el nombre completo del estudiante
            .all()
        )

        # Formatear los resultados en un diccionario
        resultados = []
        for row in query:
            # Convertir la nota final a float si es decimal
            nota_final = float(row.notfinal) if isinstance(row.notfinal, Decimal) else row.notfinal

            # Agregar cada fila a la lista de resultados
            resultados.append({
                'insid': row.insid,
                'curnombre': row.curnombre,
                'curfchini': row.curfchini.isoformat() if row.curfchini else None,
                'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'pernomcompletodocente': row.pernomcompletodocente,
                'pernrodocdocente': row.pernrodocdocente,
                'matnombre': row.matnombre,
                'peridestudiante': row.peridestudiante,
                'pernomcompleto': row.pernomcompleto,
                'perapepat': row.perapepat,
                'perapemat': row.perapemat,
                'pernombres': row.pernombres,
                'pernrodoc': row.pernrodoc,
                'perfoto': row.perfoto,
                'notid': row.notid,
                'not1': row.not1,
                'not2': row.not2,
                'not3': row.not3,
                'notfinal': nota_final,
                'notusureg': row.notusureg,
                'notfecreg': row.notfecreg.isoformat() if row.notfecreg else None,
                'notusumod': row.notusumod,
                'notfecmod': row.notfecmod.isoformat() if row.notfecmod else None,
                'estado': row.estado
            })

        # Generar el reporte en PDF utilizando el formato que ya tienes definido
        return make(Report().RptNotaCursoMateria(resultados, data['usuname']))

    except Exception as e:
        print(f"Error rptNotaCursoMateria: {e}")
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

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
            # Contar el número de estudiantes
            func.count(i.insid).label('num_estudiantes')
        )
            .outerjoin(c, c.curid == cm.curid)
            .outerjoin(m, m.matid == cm.matid)
            .outerjoin(p, p.perid == cm.periddocente)
            # Unir con la tabla de inscripciones
            .outerjoin(i, i.curmatid == cm.curmatid)
            # Agrupar por ID único de la combinación
            .group_by(cm.curmatid, c.curid, m.matid, p.perid)
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
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
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
