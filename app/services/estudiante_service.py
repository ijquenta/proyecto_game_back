from core.database import select, execute, execute_function, execute_response, as_string
from psycopg2 import sql
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
        u.usuid, u.usuname, u.usuemail, u.usuimagen  
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
    lista_obtenerMateriasInscritas = select(f'''
        SELECT distinct i.insid, i.matrid, tm.tipmatrgestion, i.curmatid, c.curnombre,cm.curmatfecini, cm.curmatfecfin, cm.periddocente, p.pernomcompleto, m2.matnombre, i.peridestudiante, i.pagid, i.insusureg, i.insfecreg, 
        i.insusumod, i.insfecmod, i.insestado, i.insestadodescripcion
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.persona p on p.perid = cm.periddocente
        left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
        where i.peridestudiante = {data['perid']}
    ''')
    for materia_inscrita in lista_obtenerMateriasInscritas:
        materia_inscrita["insfecreg"] = darFormatoFechaConHora(materia_inscrita["insfecreg"])
        materia_inscrita["insfecmod"] = darFormatoFechaConHora(materia_inscrita["insfecmod"])
        materia_inscrita["curmatfecini"] = darFormatoFechaSinHora(materia_inscrita["curmatfecini"])
        materia_inscrita["curmatfecfin"] = darFormatoFechaSinHora(materia_inscrita["curmatfecfin"])
    return lista_obtenerMateriasInscritas

