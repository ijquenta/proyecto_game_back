from flask import jsonify, make_response
from utils.date_formatting import *
from http import HTTPStatus
from core.database import db
from utils.date_formatting import darFormatoFechaSinHorav2
from models.curso_materia_model import CursoMateria
from models.curso_model import Curso
from models.materia_model import Materia
from models.persona_model import Persona
from models.inscripcion_model import Inscripcion
from sqlalchemy.exc import SQLAlchemyError 
from sqlalchemy.orm import aliased


def getListCursoMateriaContabilidad(data):
    try:
        # Se formatean las fechas de inicio y fin usando la función `darFormatoFechaSinHorav2`
        fecini = darFormatoFechaSinHorav2(data['fecini'])
        fecfin = darFormatoFechaSinHorav2(data['fecfin'])

        # Se crean alias para las tablas para hacer más legible la consulta
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)

        # Se construye una subconsulta para contar el número de estudiantes inscritos
        subquery_num_estudiantes = (
            db.session.query(
                i.curmatid,
                db.func.count(i.peridestudiante).label('numest')
            )
            .filter(i.insestado == 1)  # Filtra inscripciones activas
            .group_by(i.curmatid)  # Agrupa por el ID del curso-materia
            .subquery()  # Convierte la consulta en una subconsulta
        )

        # Se construye la consulta principal
        query = (
            db.session.query(
                cm.curmatid,  # ID del curso-materia
                cm.curid,  # ID del curso
                c.curnombre,  # Nombre del curso
                cm.matid,  # ID de la materia
                m.matnombre,  # Nombre de la materia
                cm.periddocente,  # ID del docente
                p.pernomcompleto,  # Nombre completo del docente
                p.perfoto,  # Foto del docente
                cm.curmatfecini,  # Fecha de inicio del curso-materia
                cm.curmatfecfin,  # Fecha de fin del curso-materia
                cm.curmatcosto,  # Costo del curso-materia
                subquery_num_estudiantes.c.numest.label('numero_estudiantes')  # Número de estudiantes inscritos
            )
            # Se unen las tablas utilizando las relaciones entre ellas
            .outerjoin(c, c.curid == cm.curid)  # Une con la tabla de cursos
            .outerjoin(m, m.matid == cm.matid)  # Une con la tabla de materias
            .outerjoin(p, p.perid == cm.periddocente)  # Une con la tabla de personas (docentes)
            .outerjoin(subquery_num_estudiantes, subquery_num_estudiantes.c.curmatid == cm.curmatid)  # Une con la subconsulta
            # Se agregan las condiciones de filtrado
            .filter(
                cm.curmatfecini > fecini,  # Filtra cursos-materia que comiencen después de la fecha inicial
                cm.curmatfecfin < fecfin,  # Filtra cursos-materia que terminen antes de la fecha final
                cm.curmatestado == 1  # Filtra cursos-materia que estén activos
            )
            .all()  # Ejecuta la consulta y obtiene todos los resultados
        )
        
        # Se crea una lista de diccionarios con los resultados de la consulta
        lista_cm = [
            {
                'curmatid': row.curmatid,  # ID del curso-materia
                'curid': row.curid,  # ID del curso
                'curnombre': row.curnombre,  # Nombre del curso
                'matid': row.matid,  # ID de la materia
                'matnombre': row.matnombre,  # Nombre de la materia
                'periddocente': row.periddocente,  # ID del docente
                'pernomcompleto': row.pernomcompleto,  # Nombre completo del docente
                'perfoto': row.perfoto,  # Foto del docente
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,  # Fecha de inicio en formato ISO
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,  # Fecha de fin en formato ISO
                'curmatcosto': row.curmatcosto,  # Costo del curso-materia
                'numero_estudiantes': row.numero_estudiantes  # Número de estudiantes inscritos
            } for row in query  # Itera sobre cada fila del resultado de la consulta
        ]

        # Se retorna la lista en formato JSON con un código de respuesta HTTP 200 (OK)
        return make_response(jsonify(lista_cm), HTTPStatus.OK)

    except SQLAlchemyError as e:
        # En caso de error, se deshacen los cambios y se captura el error
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e)  # Se agrega el mensaje de error
        }
        # Se retorna un mensaje de error en formato JSON con un código de respuesta HTTP 500 (Internal Server Error)
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        # Finalmente, se cierra la sesión de la base de datos
        db.session.close()


def getListCursoMateriaContabilidad(data):
    try:
        # Se formatean las fechas de inicio y fin usando la función `darFormatoFechaSinHorav2`
        fecini = darFormatoFechaSinHorav2(data['fecini'])
        fecfin = darFormatoFechaSinHorav2(data['fecfin'])

        # Se crean alias para las tablas para hacer más legible la consulta
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)

        # Se construye una subconsulta para contar el número de estudiantes inscritos
        subquery_num_estudiantes = (
            db.session.query(
                i.curmatid,
                db.func.count(i.peridestudiante).label('numest')
            )
            .filter(i.insestado == 1)  # Filtra inscripciones activas
            .group_by(i.curmatid)  # Agrupa por el ID del curso-materia
            .subquery()  # Convierte la consulta en una subconsulta
        )

        # Se construye la consulta principal
        query = (
            db.session.query(
                cm.curmatid,  # ID del curso-materia
                cm.curid,  # ID del curso
                c.curnombre,  # Nombre del curso
                cm.matid,  # ID de la materia
                m.matnombre,  # Nombre de la materia
                cm.periddocente,  # ID del docente
                p.pernomcompleto,  # Nombre completo del docente
                p.perfoto,  # Foto del docente
                cm.curmatfecini,  # Fecha de inicio del curso-materia
                cm.curmatfecfin,  # Fecha de fin del curso-materia
                cm.curmatcosto,  # Costo del curso-materia
                subquery_num_estudiantes.c.numest.label('numero_estudiantes')  # Número de estudiantes inscritos
            )
            # Se unen las tablas utilizando las relaciones entre ellas
            .outerjoin(c, c.curid == cm.curid)  # Une con la tabla de cursos
            .outerjoin(m, m.matid == cm.matid)  # Une con la tabla de materias
            .outerjoin(p, p.perid == cm.periddocente)  # Une con la tabla de personas (docentes)
            .outerjoin(subquery_num_estudiantes, subquery_num_estudiantes.c.curmatid == cm.curmatid)  # Une con la subconsulta
            # Se agregan las condiciones de filtrado
            .filter(
                cm.curmatfecini > fecini,  # Filtra cursos-materia que comiencen después de la fecha inicial
                cm.curmatfecfin < fecfin,  # Filtra cursos-materia que terminen antes de la fecha final
                cm.curmatestado == 1  # Filtra cursos-materia que estén activos
            )
            .all()  # Ejecuta la consulta y obtiene todos los resultados
        )
        
        # Se crea una lista de diccionarios con los resultados de la consulta
        lista_cm = [
            {
                'curmatid': row.curmatid,  # ID del curso-materia
                'curid': row.curid,  # ID del curso
                'curnombre': row.curnombre,  # Nombre del curso
                'matid': row.matid,  # ID de la materia
                'matnombre': row.matnombre,  # Nombre de la materia
                'periddocente': row.periddocente,  # ID del docente
                'pernomcompleto': row.pernomcompleto,  # Nombre completo del docente
                'perfoto': row.perfoto,  # Foto del docente
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,  # Fecha de inicio en formato ISO
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,  # Fecha de fin en formato ISO
                'curmatcosto': row.curmatcosto,  # Costo del curso-materia
                'numero_estudiantes': row.numero_estudiantes  # Número de estudiantes inscritos
            } for row in query  # Itera sobre cada fila del resultado de la consulta
        ]

        # Se retorna la lista en formato JSON con un código de respuesta HTTP 200 (OK)
        return make_response(jsonify(lista_cm), HTTPStatus.OK)

    except SQLAlchemyError as e:
        # En caso de error, se deshacen los cambios y se captura el error
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e)  # Se agrega el mensaje de error
        }
        # Se retorna un mensaje de error en formato JSON con un código de respuesta HTTP 500 (Internal Server Error)
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        # Finalmente, se cierra la sesión de la base de datos
        db.session.close()


def getListCursoMateriaContabilidadById(data):
    try:
        # Se extraen los valores de curid y matid desde los datos proporcionados
        curid = data.get('curid')
        matid = data.get('matid')

        # Se crean alias para las tablas para hacer más legible la consulta
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)

        # Se construye una subconsulta para contar el número de estudiantes inscritos
        subquery_num_estudiantes = (
            db.session.query(
                i.curmatid,
                db.func.count(i.peridestudiante).label('numest')
            )
            .filter(i.insestado == 1)  # Filtra inscripciones activas
            .group_by(i.curmatid)  # Agrupa por el ID del curso-materia
            .subquery()  # Convierte la consulta en una subconsulta
        )

        # Se construye la consulta principal
        query = (
            db.session.query(
                cm.curmatid,  # ID del curso-materia
                cm.curid,  # ID del curso
                c.curnombre,  # Nombre del curso
                cm.matid,  # ID de la materia
                m.matnombre,  # Nombre de la materia
                cm.periddocente,  # ID del docente
                p.pernomcompleto,  # Nombre completo del docente
                p.perfoto,  # Foto del docente
                cm.curmatfecini,  # Fecha de inicio del curso-materia
                cm.curmatfecfin,  # Fecha de fin del curso-materia
                cm.curmatcosto,  # Costo del curso-materia
                subquery_num_estudiantes.c.numest.label('numero_estudiantes')  # Número de estudiantes inscritos
            )
            # Se unen las tablas utilizando las relaciones entre ellas
            .outerjoin(c, c.curid == cm.curid)  # Une con la tabla de cursos
            .outerjoin(m, m.matid == cm.matid)  # Une con la tabla de materias
            .outerjoin(p, p.perid == cm.periddocente)  # Une con la tabla de personas (docentes)
            .outerjoin(subquery_num_estudiantes, subquery_num_estudiantes.c.curmatid == cm.curmatid)  # Une con la subconsulta
            # Se agregan las condiciones de filtrado
            .filter(
                cm.curid == curid if curid is not None else True,  # Filtra por el ID del curso si se proporciona
                cm.matid == matid if matid is not None else True,  # Filtra por el ID de la materia si se proporciona
                cm.curmatestado == 1  # Filtra cursos-materia que estén activos
            )
            .all()  # Ejecuta la consulta y obtiene todos los resultados
        )
        
        # Se crea una lista de diccionarios con los resultados de la consulta
        lista_cm = [
            {
                'curmatid': row.curmatid,  # ID del curso-materia
                'curid': row.curid,  # ID del curso
                'curnombre': row.curnombre,  # Nombre del curso
                'matid': row.matid,  # ID de la materia
                'matnombre': row.matnombre,  # Nombre de la materia
                'periddocente': row.periddocente,  # ID del docente
                'pernomcompleto': row.pernomcompleto,  # Nombre completo del docente
                'perfoto': row.perfoto,  # Foto del docente
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,  # Fecha de inicio en formato ISO
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,  # Fecha de fin en formato ISO
                'curmatcosto': row.curmatcosto,  # Costo del curso-materia
                'numero_estudiantes': row.numero_estudiantes  # Número de estudiantes inscritos
            } for row in query  # Itera sobre cada fila del resultado de la consulta
        ]

        # Se retorna la lista en formato JSON con un código de respuesta HTTP 200 (OK)
        return make_response(jsonify(lista_cm), HTTPStatus.OK)

    except SQLAlchemyError as e:
        # En caso de error, se deshacen los cambios y se captura el error
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e)  # Se agrega el mensaje de error
        }
        # Se retorna un mensaje de error en formato JSON con un código de respuesta HTTP 500 (Internal Server Error)
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        # Finalmente, se cierra la sesión de la base de datos
        db.session.close()
