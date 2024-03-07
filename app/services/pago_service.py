from core.database import select, execute, execute_function, execute_response
from web.wsrrhh_service import *
from flask import Flask, request, jsonify, make_response

def listarPago():
    return select('''
        SELECT pagid, pagdescripcion, pagestadodescripcion, pagmonto, pagdoc, pagrusureg, pagrfecreg, pagrusumod, pagrfecmod, pagestado FROM academico.pago;
    ''')

def gestionarPago(data):
    data = {key: f'\'{value}\'' if value is not None else 'NULL' for key, value in data.items()}

    return execute_function(f'''
       SELECT academico.f_gestionar_pago
               ({data['tipo']},
                {data['pagid']}, 
                {data['insid']}, 
                {data['pagdescripcion']}, 
                {data['pagmonto']}, 
                {data['pagfecha']},
                {data['pagrusureg']},
                {data['pagestadodescripcion']}, 
                {data['pagestado']}) as valor;
    ''')

def listarPagoEstudiante(data):
    return select(f'''
        SELECT i.insid, i.matrid, cm.curid, c.curnombre, cm.matid, m.matnombre, i.peridestudiante, i.pagid, i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion 
        FROM academico.inscripcion i
        left join academico.curso_materia cm on cm.curmatid = i.curmatid
        left join academico.curso c on c.curid = cm.curid
        left join academico.materia m on m.matid = cm.matid
        where i.peridestudiante = {data['perid']}
        order by c.curnombre, m.matnombre; 
    ''') 

def listarPagoEstudianteMateria(data):
    return select(f'''
       SELECT distinct i.insid, i.matrid, m.matrgestion, i.curmatid, c.curnombre, m2.matnombre, i.peridestudiante, 
                i.pagid, p.pagdescripcion, p.pagestadodescripcion, p.pagmonto, p.pagdoc, pagrusureg, pagrfecreg, pagrusumod, pagrfecmod, pagestado 
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.pago p on p.pagid = i.pagid
        where i.peridestudiante = {data['perid']}
        and cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
    ''') 

def listarPagoCurso():
    return select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        order by c.curnombre, m.matnombre; 
    ''')   
    
def listarPagoEstudiantesMateria(data):
    return select(f'''
       SELECT distinct i.insid, i.matrid, m.matrgestion, i.curmatid, c.curnombre, m2.matnombre, i.peridestudiante, p2.pernomcompleto,
                i.pagid, p.pagdescripcion, p.pagestadodescripcion, p.pagmonto, p.pagdoc, pagrusureg, pagrfecreg, pagrusumod, pagrfecmod, pagestado 
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.pago p on p.pagid = i.pagid
        left join academico.persona p2 on p2.perid = i.peridestudiante 
        where cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
    ''') 