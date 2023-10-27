from core.database import select, as_string, execute, execute_function
from psycopg2 import sql

def listarCursoMateria():
    return select(f'''
    SELECT curmatid, c.curnombre , cm.curid, m.matnombre, cm.matid, p.pernombres, p.perapepat, p.perapemat, cm.periddocente, curmatfecini, curmatfecfin, curmatestado, curmatusureg, curmatfecreg, curmatusumod, curmatfecmod
    FROM academico.curso_materia cm
    inner join academico.curso c on c.curid  = cm.curid 
    inner join academico.materia m on m.matid = cm.matid 
    inner join academico.persona p on p.perid = cm.periddocente 
    order by curid;       
    ''')

def listaCursoCombo():
    return select(f'''
    SELECT curid, curnombre, curnivel
    FROM academico.curso
    where curestadodescripcion = 'Vigente'
    order by curnivel      
    ''')

def listaPersonaDocenteCombo(data):
    return select(f'''
    select pe.perid, pe.pernombres, pe.perapepat, pe.perapemat 
    from academico.persona pe 
    inner join academico.roles r ON r.rolid = pe.peridrol
    where r.rolnombre = \'{data['rolnombre']}\'  
    ''')
    