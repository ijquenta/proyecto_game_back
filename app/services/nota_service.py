from core.database import select, execute, execute_function, execute_response
from web.wsrrhh_service import *
from core.rml.report_generator import Report
from flask import make_response

def make(pdf):
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format("archivo.pdf")
    response.mimetype = 'application/pdf'
    return response

def listarNota():
    return select('''
        SELECT notid, insid, not1, not2, not3, notfinal, notusureg, notfecreg, notusumod, notfecmod, notestado FROM academico.nota;
    ''')
 
def listarNotaEstudiante(data):
    return select(f'''
        SELECT i.insid, i.matrid, cm.curid, c.curnombre, cm.matid, m.matnombre, i.peridestudiante, i.pagid, i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion 
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid
        left join academico.materia m on m.matid = cm.matid
        where i.peridestudiante = {data['perid']}
        order by c.curnombre, m.matnombre; 
    ''')   

def listarNotaDocente(data):
    return select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        where cm.periddocente = {data['perid']}
        order by c.curnombre, m.matnombre; 
    ''')   
    

    
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
    return select(f'''
        SELECT i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto, n.notid, n.not1, n.not2, n.not3, n.notfinal, n.notusureg, n.notfecreg, n.notusumod, n.notfecmod
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.nota n on n.insid = i.insid
        where i.curmatid = {data['curmatid']}
        order by p.pernomcompleto;
    ''')  


def rptNotaEstudianteMateria(data):
    print("data", data)
    params = select(f'''
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
        order by c.curnombre, m.matnombre
    ''')
    print("params", params)
    return make(Report().RptNotaEstudianteMateria(params, data['usuname']))