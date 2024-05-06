from core.database import select, execute, execute_function, execute_response
from utils.date_formatting import *

def obtenerMateriasAsignadas(data):
    lista_materias_asignadas = select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.matid, m2.matnombre, cm.periddocente, p.pernomcompleto,
        cm.curmatfecini, 
        cm.curmatfecfin, cm.curmatestado, cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, 
        cm.curmatestadodescripcion, cm.curmatidrol, cm.curmatidroldes, cm.curmatdescripcion 
        FROM academico.curso_materia cm
        inner join academico.persona p on p.perid = cm.periddocente
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        where cm.periddocente = {data['perid']}
    ''')
    for materia_asignada in lista_materias_asignadas:
        materia_asignada['curmatfecini'] = darFormatoFechaSinHora(materia_asignada['curmatfecini'])
        materia_asignada['curmatfecfin'] = darFormatoFechaSinHora(materia_asignada['curmatfecfin'])
        materia_asignada['curmatfecreg'] = darFormatoFechaConHora(materia_asignada['curmatfecreg'])
        materia_asignada['curmatfecmod'] = darFormatoFechaConHora(materia_asignada['curmatfecmod'])
    return lista_materias_asignadas

def listarMateriaEstudianteCurso(data):
    return select(f'''
        SELECT i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = i.peridestudiante
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

