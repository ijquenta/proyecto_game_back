from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from utils.date_formatting import *

def listarInscripcion():
    lista_inscripciones = select(f'''
        SELECT 
        distinct
        i.insid, 
        i.matrid, m.tipmatrid, tm.tipmatrgestion, m.matrestado, m.matrdescripcion,   
        i.peridestudiante, p.pernomcompleto as pernombrecompletoestudiante, p.perfoto, 
        i.pagid, p2.pagdescripcion,  p2.pagtipo, p2.pagmonto, p2.pagfecha, p2.pagarchivo,
        i.curmatid, cm.curid, cm.curmatdescripcion, c.curnombre, cm.matid, 
        cm.curmatfecini, cm.curmatfecfin,
        m2.matnombre,
        cm.periddocente, p3.pernomcompleto as pernombrecompletodocente, p3.perfoto as perfotodocente,
        i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, 
        i.insestado, i.insestadodescripcion
        FROM academico.inscripcion i
        left join academico.matricula m on i.matrid = m.matrid
        left join academico.persona p on i.peridestudiante = p.perid 
        left join academico.pago p2 on i.pagid = p2.pagid
        left join academico.curso_materia cm on i.curmatid = cm.curmatid   
        left join academico.curso c on cm.curid = c.curid
        left join academico.materia m2 on cm.matid = m2.matid
        left join academico.persona p3 on cm.periddocente = p3.perid
        left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
        order by i.insid desc;
    ''')
    for curso in lista_inscripciones:
        curso["insfecreg"] = darFormatoFechaConHora(curso["insfecreg"])
        curso["insfecmod"] = darFormatoFechaConHora(curso["insfecmod"])
        curso["curmatfecini"] = darFormatoFechaSinHora(curso["curmatfecini"])
        curso["curmatfecfin"] = darFormatoFechaSinHora(curso["curmatfecfin"])
    return lista_inscripciones
   
def listarComboCursoMateria():
    lista_comboCursoMateria = select('''
        SELECT DISTINCT  
            cm.curmatid,
            c.curnombre,
            m.matnombre,
            cm.curmatfecini,
            cm.curmatfecfin
        FROM academico.curso_materia cm
        LEFT JOIN academico.curso c ON c.curid = cm.curid 
        LEFT JOIN academico.materia m ON m.matid = cm.matid;
    ''')

    resultado = []

    for cursoCombo in lista_comboCursoMateria:
        curmatdescripcion = f'{cursoCombo["curnombre"]} - {cursoCombo["matnombre"]} - { darFormatoFechaSinHora(cursoCombo["curmatfecini"])} a { darFormatoFechaSinHora(cursoCombo["curmatfecfin"])}'
        resultado.append({"curmatid": cursoCombo["curmatid"], "curmatdescripcion": curmatdescripcion})

    resultado.sort(key=lambda x: x["curmatdescripcion"])
    return resultado

def listarComboMatriculaEstudiante(data):
    return select(f'''
    select m.matrid, m.tipmatrid, tm.tipmatrgestion, m.peridestudiante, p.pernomcompleto, p.perfoto
    from academico.matricula m
    left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
    left join academico.persona p on p.perid = m.peridestudiante
    where m.peridestudiante = {data['peridestudiante']}
    and m.matrestado = 1    
    order by tm.tipmatrgestion;
    ''')

def listarComboMatricula():
    return select(f'''
    SELECT matrid, matrgestion
    FROM academico.matricula
    WHERE matrestado = 1
    order by matrgestion desc;
    ''')
    
def obtenerCursoMateria(data):
    return select(f'''
    SELECT cm.curmatid
    FROM academico.curso_materia cm
    where cm.curid = {data['curid']} 
    and cm.matid = {data['matid']}
    ''')
    
def insertarInscripcion(data):
    if data['pagid'] is not None:
        pagid = data['pagid']
    else:
        pagid = 'null'

    return execute_function(f'''
    SELECT academico.insertar_inscripcion(
          {data['matrid']}, 
          {data['peridestudiante']}, 
          {pagid}, 
        \'{data['insusureg']}\',
          {data['curmatid']}, 
          {data['insestado']}, 
        \'{data['insestadodescripcion']}\')  as valor;                      
    ''')

def modificarInscripcion(data):
    if data['pagid'] is not None:
        pagid = data['pagid']
    else:
        pagid = 'null'
    return execute_function(f'''
    SELECT academico.modificar_inscripcion(
          {data['insid']}, 
          {data['matrid']}, 
          {data['peridestudiante']}, 
          {pagid}, 
        \'{data['insusumod']}\',
          {data['curmatid']}, 
          {data['insestado']}, 
        \'{data['insestadodescripcion']}\')  as valor;                      
    ''')  

def eliminarInscripcion(data):
    return execute_function(f'''
    SELECT academico.eliminar_inscripcion(
        {data['insid']})  as valor;                      
    ''') 
    
def gestionarInscripcionEstado(data):
    return execute_function(f'''
    SELECT academico.f_inscripcion_gestionar_estado(
          {data['tipo']},    
          {data['insid']},    
          \'{data['insusumod']}\'
    ) as valor;
    ''')

def obtenerEstudiantesInscritos(data):
    return select(f'''
    select peridestudiante as perid 
    from academico. inscripcion i
    where curmatid = {data['curmatid']}
    and i.insestado = 1
    ''')
    
    
    
    
    