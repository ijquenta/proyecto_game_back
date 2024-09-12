from core.database import select
from utils.date_formatting import *
from models.curso_materia_model import CursoMateria
from models.persona_model import Persona 
from models.materia_model import Materia, db
from models.curso_model import Curso
from models.inscripcion_model import Inscripcion
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, make_response
from http import HTTPStatus
from sqlalchemy.sql import func

def obtenerMateriasAsignadas(data):
    try:
        perid = data.get('perid')

        # Crear alias para las tablas si es necesario
        cm = aliased(CursoMateria)
        p = aliased(Persona)
        m2 = aliased(Materia)
        c = aliased(Curso)
        ins = aliased(Inscripcion)

        # Ejecutar la consulta
        query = (db.session.query(
                    cm.curmatid,
                    cm.curid,
                    c.curnombre,
                    c.curfchini,
                    c.curfchfin,
                    cm.matid,
                    m2.matnombre,
                    cm.periddocente,
                    p.pernomcompleto,
                    cm.curmatfecini,
                    cm.curmatfecfin,
                    cm.curmatestado,
                    cm.curmatusureg,
                    cm.curmatfecreg,
                    cm.curmatusumod,
                    cm.curmatfecmod,
                    cm.curmatestadodescripcion,
                    cm.curmatidrol,
                    cm.curmatidroldes,
                    cm.curmatdescripcion,
                    func.coalesce(func.count(ins.peridestudiante), 0).label('numero_estudiantes')
                )
                .select_from(cm)
                .join(p, p.perid == cm.periddocente)
                .outerjoin(m2, m2.matid == cm.matid)
                .outerjoin(c, c.curid == cm.curid)
                .outerjoin(ins, ins.curmatid == cm.curmatid)
                .group_by(
                    cm.curmatid,
                    cm.curid,
                    c.curnombre,
                    c.curfchini,
                    c.curfchfin,
                    cm.matid,
                    m2.matnombre,
                    cm.periddocente,
                    p.pernomcompleto,
                    cm.curmatfecini,
                    cm.curmatfecfin,
                    cm.curmatestado,
                    cm.curmatusureg,
                    cm.curmatfecreg,
                    cm.curmatusumod,
                    cm.curmatfecmod,
                    cm.curmatestadodescripcion,
                    cm.curmatidrol,
                    cm.curmatidroldes,
                    cm.curmatdescripcion
                )
                .filter(cm.periddocente == perid)
                .all())

        # Convertir resultados a formato JSON
        lista_materias_asignadas = [
            { 
             'curmatid': row.curmatid,
             'curid': row.curid,
             'curfchini': row.curfchini.isoformat() if row.curfchini else None,
             'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,
             'curnombre': row.curnombre,
             'matid': row.matid,
             'matnombre': row.matnombre,
             'periddocente': row.periddocente,
             'pernomcompleto': row.pernomcompleto,
             'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
             'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
             'curmatestado': row.curmatestado,
             'curmatusureg': row.curmatusureg,
             'curmatfecreg': row.curmatfecreg.isoformat() if row.curmatfecreg else None,
             'curmatusumod': row.curmatusumod,
             'curmatfecmod': row.curmatfecmod.isoformat() if row.curmatfecmod else None,
             'curmatestadodescripcion': row.curmatestadodescripcion,
             'curmatidrol': row.curmatidrol,
             'curmatidroldes': row.curmatidroldes,
             'curmatdescripcion': row.curmatdescripcion,
             'numero_estudiantes': row.numero_estudiantes
            } for row in query
        ]

        return make_response(jsonify(lista_materias_asignadas), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()


def listarMateriaEstudianteCurso(data):
    return select(f'''
        SELECT i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto, p.perfoto, p.pernrodoc, p.peremail, p.percelular, i.insestado, pip.pernomiglesia
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.persona_info_personal pip on pip.perid = p.perid
        where i.curmatid = {data['curmatid']}
        order by p.pernomcompleto;
    ''')  
    
def listarDocente():
    return select('''
       SELECT  distinct
        p.perid, p.pernomcompleto, p.pernombres, p.perapepat, p.perapemat, 
        p.pertipodoc, td.tipodocnombre, 
        p.pernrodoc, p.perfecnac, p.perdirec, p.peremail, p.percelular, p.pertelefono, 
        p.perpais, tp.paisnombre, 
        p.perciudad, tc.ciudadnombre,
        p.pergenero, tg.generonombre,
        p.perestcivil, te.estadocivilnombre,
        p.perfoto, p.perestado, p.perobservacion, p.perusureg, p.perfecreg, p.perusumod, p.perfecmod,
        u.usuid, u.usuname, u.usuemail  
        FROM academico.persona p
        left join academico.usuario u on u.perid = p.perid
        left join academico.rol r on r.rolid = u.rolid
        left join academico.tipo_documento td on td.tipodocid = p.pertipodoc
        left join academico.tipo_pais tp on tp.paisid = p.perpais
        left join academico.tipo_ciudad tc on tc.ciudadid = p.perciudad
        left join academico.tipo_genero tg on tg.generoid = p.pergenero
        left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil    
        where r.rolnombre = 'Docente' or r.rolnombre = 'Secretaria'
        order by p.pernomcompleto
    ''')

