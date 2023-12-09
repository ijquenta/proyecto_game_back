from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response

def listarInscripcion():
    return select(f'''
   	SELECT 
    i.insid, 
    i.matrid, m.matrgestion, m.matrestado, m.matrestadodescripcion, 
    i.peridestudiante, p.pernomcompleto as pernombrecompletoestudiante, 
    i.pagid, p2.pagdescripcion,  p2.pagestado, p2.pagestadodescripcion, p2.pagmonto, 
    i.curmatid, cm.curid, cm.curmatdescripcion, c.curnombre, cm.matid, m2.matnombre,
    cm.periddocente, p3.pernomcompleto as pernombrecompletodocente,
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
    order by i.insid desc;
    ''')
       
    
def listarComboCursoMateria():
    return select(f'''
        SELECT 
        cm.curmatid,
        c.curnombre || ' - ' || m.matnombre AS curmatdescripcion
        FROM academico.curso_materia cm
        LEFT JOIN academico.curso c ON c.curid = cm.curid 
        LEFT JOIN academico.materia m ON m.matid = cm.matid;
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
    print("Insertar Inscripcion: ", data)
    
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
    print("Modificar Inscripcion: ", data)
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
    print("Eliminar Inscripcion: ", data)
    return execute_function(f'''
    SELECT academico.eliminar_inscripcion(
        {data['insid']})  as valor;                      
    ''')  
    
    
    
    
    