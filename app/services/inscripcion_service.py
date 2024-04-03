from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from datetime import datetime

def darFormatoFechaConHora(fecha_str):
    if fecha_str is None:
       return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_formateada

def darFormatoFechaSinHora(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
    return fecha_formateada

def darFormatoFechaSinHoraAlReves(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%Y-%m-%d")
    return fecha_formateada

def listarInscripcion():
    lista_inscripciones = select(f'''
        SELECT 
        distinct
        i.insid, 
        i.matrid, m.matrgestion, m.matrestado, m.matrestadodescripcion, 
        i.peridestudiante, p.pernomcompleto as pernombrecompletoestudiante, p.perfoto, 
        i.pagid, p2.pagdescripcion,  p2.pagtipo, p2.pagmonto, p2.pagfecha, p2.pagarchivo,
        i.curmatid, cm.curid, cm.curmatdescripcion, c.curnombre, cm.matid, 
        cm.curmatfecini, cm.curmatfecfin,
        m2.matnombre,
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
    # print("lista_inscripciones: ", lista_inscripciones)
    for curso in lista_inscripciones:
        curso["insfecreg"] = darFormatoFechaConHora(curso["insfecreg"])
        curso["insfecmod"] = darFormatoFechaConHora(curso["insfecmod"])
        curso["curmatfecini"] = darFormatoFechaSinHora(curso["curmatfecini"])
        curso["curmatfecfin"] = darFormatoFechaSinHora(curso["curmatfecfin"])
    # print(lista_inscripciones)
    return lista_inscripciones

       
    
# def listarComboCursoMateria():
#     lista_comboCursoMateria = select(f'''
#         SELECT distinct  
#         cm.curmatid,
#         c.curnombre || ' - ' || m.matnombre || ' - ' || cm.curmatfecini || ' a ' || cm.curmatfecfin AS curmatdescripcion
#         FROM academico.curso_materia cm
#         LEFT JOIN academico.curso c ON c.curid = cm.curid 
#         LEFT JOIN academico.materia m ON m.matid = cm.matid;
#     ''')
#     for cursoCombo in lista_comboCursoMateria:
#         cursoCombo["curmatfecini"] = darFormatoFechaSinHora(cursoCombo["curmatfecini"])
#         cursoCombo["curmatfecfin"] = darFormatoFechaSinHora(cursoCombo["curmatfecfin"])
#     return lista_comboCursoMateria
   
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

    # Ordenar la lista por curmatdescripcion
    resultado.sort(key=lambda x: x["curmatdescripcion"])
    return resultado





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
    
    
    
    
    