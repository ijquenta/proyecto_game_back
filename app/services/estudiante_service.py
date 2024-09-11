from http import HTTPStatus

from flask import jsonify, make_response

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from sqlalchemy import case

from core.database import db, select, execute_function

from models.curso_model import Curso
from models.curso_materia_model import CursoMateria
from models.inscripcion_model import Inscripcion
from models.materia_model import Materia
from models.matricula_model import Matricula
from models.persona_model import Persona, PersonaInfoPersonal, PersonaInfoAcademica, PersonaInfoMinisterial, TipoProfesion, TipoEstadoCivil, TipoEducacion, TipoCargo
from models.tipo_matricula_model import TipoMatricula


from utils.date_formatting import *


def listarEstudiante():
    return select('''
        SELECT p.perid, p.pernomcompleto, p.pernombres, p.perapepat, p.perapemat, 
        p.pertipodoc, td.tipodocnombre, 
        p.pernrodoc, p.perfecnac, p.perdirec, p.peremail, p.percelular, p.pertelefono, 
        p.perpais, tp.paisnombre, 
        p.perciudad, tc.ciudadnombre,
        p.pergenero, tg.generonombre,
        p.perestcivil, te.estadocivilnombre,
        p.perfoto, p.perestado, p.perobservacion, p.perusureg, p.perfecreg, p.perusumod, p.perfecmod, p.pernrohijos, p.perprofesion, p.perfeclugconversion,
        p.perbautismoaguas, p.perbautismoespiritu, p.pernomdiriglesia, p.pernompastor,
        u.usuid, u.usuname, u.usuemail 
        FROM academico.persona p
        left join academico.usuario u on u.perid = p.perid
        left join academico.rol r on r.rolid = u.rolid
        left join academico.tipo_documento td on td.tipodocid = p.pertipodoc
        left join academico.tipo_pais tp on tp.paisid = p.perpais
        left join academico.tipo_ciudad tc on tc.ciudadid = p.perciudad
        left join academico.tipo_genero tg on tg.generoid = p.pergenero
        left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil    
        where r.rolnombre = 'Estudiante'
        order by p.pernomcompleto
    ''')

def obtenerMateriasInscritas(data):
    try:
        # Definir alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)
        mtr = aliased(Matricula)
        tm = aliased(TipoMatricula)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
            i.insid,
            i.matrid,
            i.curmatid,
            c.curnombre,
            m.matnombre,
            c.curfchini,
            c.curfchfin,
            cm.curmatfecini,
            cm.curmatestado,
            cm.curmatfecfin,
            cm.periddocente,
            p.pernomcompleto,
            p.pernrodoc,
            p.perfoto,
            i.peridestudiante,
            i.pagid,
            i.insusureg,
            i.insfecreg,
            i.insusumod,
            i.insfecmod,
            i.insestado,
            i.insestadodescripcion,
            mtr.pagoidmatricula,
            tm.tipmatrgestion 
        )
            .distinct()
            .outerjoin(mtr, i.matrid == mtr.matrid)
            .outerjoin(cm, cm.curmatid == i.curmatid)
            .outerjoin(m, m.matid == cm.matid)
            .outerjoin(c, c.curid == cm.curid)
            .outerjoin(p, p.perid == cm.periddocente)
            .outerjoin(tm, tm.tipmatrid == mtr.tipmatrid)
            .filter(i.peridestudiante == data['perid'])
            .all())

        # Convertir los resultados en una lista de diccionarios
        lista_materias_inscritas = [
            {
                'insid': row.insid,
                'matrid': row.matrid,
                'curmatid': row.curmatid,
                'curnombre': row.curnombre,
                'matnombre': row.matnombre,
                'curfchini': row.curfchini.isoformat() if row.curfchini else None,
                'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatestado': row.curmatestado,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'periddocente': row.periddocente,
                'pernomcompleto': row.pernomcompleto,
                'pernrodoc': row.pernrodoc,
                'perfoto': row.perfoto,
                'peridestudiante': row.peridestudiante,
                'pagid': row.pagid,
                'insusureg': row.insusureg,
                'insfecreg': row.insfecreg.isoformat() if row.insfecreg else None,
                'insusumod': row.insusumod,
                'insfecmod': row.insfecmod.isoformat() if row.insfecmod else None,
                'insestado': row.insestado,
                'insestadodescripcion': row.insestadodescripcion,
                'pagoidmatricula': row.pagoidmatricula,
                'tipmatrgestion': row.tipmatrgestion 
            } for row in query
        ]

        return make_response(jsonify(lista_materias_inscritas), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

# Actualizar datos personales
def actualizarDatosPersonales(data):
    res = execute_function(f'''
       SELECT academico.f_persona_actualizar_datos_personal (
                {data['perid']},
                \'{data['perusumod']}\',
                {data['pernrohijos']},
                \'{data['perprofesion']}\',
                \'{data['perfeclugconversion']}\',
                {data['perbautismoaguas']},
                {data['perbautismoespiritu']},
                \'{data['pernomdiriglesia']}\',
                \'{data['pernompastor']}\'  
                ) as valor;
    ''')
    return res

def getInformacionDocente(data):
    try:
        pip = aliased(PersonaInfoPersonal)
        tp = aliased(TipoProfesion)
        tec = aliased(TipoEstadoCivil)
        pia = aliased(PersonaInfoAcademica)
        te = aliased(TipoEducacion)
        pim = aliased(PersonaInfoMinisterial)
        tc = aliased(TipoCargo)
        p = aliased(Persona)
        
        # Consulta de información personal y docente
        row = (db.session.query(
            pip.perid,
            p.pernomcompleto,
            p.perfoto,
            p.perfecnac,
            p.pernrodoc,
            p.perdirec,
            tec.estadocivilnombre,
            p.percelular,
            p.pertelefono,
            p.peremail,
            pip.peredad,
            pip.perprofesion,
            tp.pronombre,
            pip.perfecconversion,
            pip.perlugconversion,
            case([(pip.perbautizoagua != None, 'Sí')], else_='No').label('perbautizoagua'),
            case([(pip.perbautizoespiritu != None, 'Sí')], else_='No').label('perbautizoespiritu'),
            pip.pernomiglesia,
            pip.perdiriglesia,
            pip.perexperiencia,
            pip.permotivo,
            pip.perplanesmetas
        ).join(tp, tp.proid == pip.perprofesion)
         .join(p, p.perid == pip.perid)
         .outerjoin(TipoEstadoCivil, TipoEstadoCivil.estadocivilid == p.perestcivil)
         .filter(pip.perid == data['perid'])
         .first())  # Solo se espera un resultado
 
        # Verificar si se encontró el resultado
        if not row:
            return make_response(jsonify({"error": "No hay Información del Docente"}), HTTPStatus.NOT_FOUND)
        
        # Consulta de información académica
        academica = db.session.query(
            pia.perinfoaca,
            pia.perid,
            pia.pereducacion,
            te.edunombre,
            pia.pernominstitucion,
            pia.perdirinstitucion,
            pia.pergescursadas,
            pia.perfechas,
            pia.pertitulo
        ).join(te, te.eduid == pia.pereducacion)\
         .filter(pia.perid == data['perid'])\
         .order_by(te.edunombre)\
         .all()

        # Consulta de información ministerial
        ministerial = db.session.query(
            pim.perinfomin,
            pim.perid,
            pim.pernomiglesia,
            pim.percargo,
            tc.carnombre,
            pim.pergestion
        ).join(tc, tc.carid == pim.percargo)\
         .filter(pim.perid == data['perid'])\
         .order_by(pim.pernomiglesia)\
         .all()
        
        # Construir la respuesta final
        docente = {
            'persona': {
                'perid': row.perid,
                'pernomcompleto': row.pernomcompleto,
                'perfoto': row.perfoto, 
                'perfecnac': row.perfecnac.isoformat() if row.perfecnac else None,
                'pernrodoc': row.pernrodoc,
                'perdirec': row.perdirec,
                'peremail': row.peremail,
                'estadocivilnombre': row.estadocivilnombre,
                'percelular': row.percelular,
                'pertelefono': row.pertelefono,
                'peredad': row.peredad,
                'perprofesion': row.perprofesion,
                'pronombre': row.pronombre,
                'perfecconversion': row.perfecconversion.isoformat() if row.perfecconversion else None,
                'perlugconversion': row.perlugconversion,
                'perbautizoagua': row.perbautizoagua,
                'perbautizoespiritu': row.perbautizoespiritu,
                'pernomiglesia': row.pernomiglesia,
                'perdiriglesia': row.perdiriglesia,
                'perexperiencia': row.perexperiencia,
                'permotivo': row.permotivo,
                'perplanesmetas': row.perplanesmetas
            },
            'infoAcademica': [
                {
                    'perinfoaca': aca.perinfoaca,
                    'pereducacion': aca.pereducacion,
                    'edunombre': aca.edunombre,
                    'pernominstitucion': aca.pernominstitucion,
                    'perdirinstitucion': aca.perdirinstitucion,
                    'pergescursadas': aca.pergescursadas,
                    'perfechas': aca.perfechas,
                    'pertitulo': aca.pertitulo
                } for aca in academica
            ],
            'infoMinisterial': [
                {
                    'perinfomin': min.perinfomin,
                    'pernomiglesia': min.pernomiglesia,
                    'carnombre': min.carnombre,
                    'pergestion': min.pergestion
                } for min in ministerial
            ]
        }
        
        return make_response(jsonify(docente), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e)
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


        