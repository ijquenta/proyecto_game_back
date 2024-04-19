from core.database import select, execute, execute_function, execute_response
from web.wsrrhh_service import *
from core.rml.report_generator import Report
from flask import make_response
from utils.date_formatting import darFormatoFechaConHora, darFormatoFechaSinHora

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

def listarNotaEstudianteCurso(data):
    return select(f'''
        SELECT i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto, p.perfoto, n.notid, n.not1, n.not2, n.not3, n.notfinal, n.notusureg, n.notfecreg, n.notusumod, n.notfecmod
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
    # print("data", data)
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
    # print("params", params)
    return make(Report().RptNotaEstudianteMateria(params, data['usuname']))


def rptNotaCursoMateria(data):
    params = select(f'''
        SELECT i.insid, c.curnombre, m.matnombre, i.peridestudiante, p.pernomcompleto, p.perfoto, n.notid, n.not1, n.not2, n.not3, n.notfinal, n.notusureg, n.notfecreg, n.notusumod, n.notfecmod
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = i.peridestudiante
        left join academico.nota n on n.insid = i.insid
        where i.curmatid = {data['curmatid']}
        order by p.pernomcompleto;
    ''')
    return make(Report().RptNotaCursoMateria(params, data['usuname']))

def listarNotaCurso():
    lista = select(f'''
        SELECT distinct cm.curmatid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, p.perfoto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        where cm.curmatestado = 1
        order by c.curnombre, m.matnombre;
    ''')  
    for pago in lista:
        pago["curmatfecreg"] = darFormatoFechaConHora(pago["curmatfecreg"])
        pago["curmatfecmod"] = darFormatoFechaConHora(pago["curmatfecmod"])
        pago["curmatfecini"] = darFormatoFechaSinHora(pago["curmatfecini"])
        pago["curmatfecfin"] = darFormatoFechaSinHora(pago["curmatfecfin"]) 
    return lista