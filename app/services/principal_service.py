from core.database import select, execute, execute_function, execute_response
from web.wsrrhh_service import *
from flask import Flask, request, jsonify, make_response
from datetime import datetime
from model.pago_model import modelPago
from utils.date_formatting import darFormatoFechaConHora, darFormatoFechaSinHora, darFormatoFechaSinHorav2



def listarEstudiantesNivel():
    return select(f'''
                   SELECT
                        c.curnivel,
                        COUNT(i.insid) AS cantidad_estudiantes
                    FROM academico.curso c
                    LEFT JOIN academico.curso_materia cm ON c.curid = cm.curid
                    LEFT JOIN academico.inscripcion i ON cm.curmatid = i.curmatid
                    GROUP BY c.curnivel
                    order by
                    c.curnivel
                  ''')

def listarEstudiantesMateria():
    return select(f'''
                  SELECT m.matnombre, COUNT(i.insid) AS cantidad_estudiantes
                    FROM academico.curso_materia cm
                    LEFT JOIN academico.inscripcion i ON cm.curmatid = i.curmatid
                    LEFT JOIN academico.materia m ON cm.matid = m.matid
                    GROUP BY m.matnombre
                    ORDER BY m.matnombre;
                  ''')
def listarCantidades():
    return select(f'''      
    SELECT
        cm.curmatnum,
        cm.curmatnum_inactivos,
        m.matnum,
        m.matnum_inactivos,
        c.nivnum,
        c.nivnum_inactivos,
        u.usunum,
        u.usunum_inactivos,
        u2.estnum,
        u2.estnum_inactivos,
        u3.docnum,
        u3.docnum_inactivos,
        u4.secnum,
        u4.secnum_inactivos,
        t.texnum,
        t.texnum_inactivos
    FROM
        (SELECT 
            COUNT(curmatid) AS curmatnum,
            SUM(1 - curmatestado) AS curmatnum_inactivos
        FROM academico.curso_materia) cm,
        (SELECT 
            COUNT(matid) AS matnum,
            SUM(1 - matestado) AS matnum_inactivos
        FROM academico.materia) m,
        (SELECT 
            COUNT(curid) AS nivnum,
            SUM(1 - curestado) AS nivnum_inactivos
        FROM academico.curso) c,
        (SELECT 
            COUNT(usuid) AS usunum,
            SUM(1 - usuestado) AS usunum_inactivos
        FROM academico.usuario) u,
        (SELECT 
            COUNT(usuid) AS estnum,
            SUM(1 - usuestado) AS estnum_inactivos
        FROM academico.usuario WHERE rolid = 4) u2,
        (SELECT 
            COUNT(usuid) AS docnum,
            SUM(1 - usuestado) AS docnum_inactivos
        FROM academico.usuario WHERE rolid = 3) u3,
        (SELECT 
            COUNT(usuid) AS secnum,
            SUM(1 - usuestado) AS secnum_inactivos
        FROM academico.usuario WHERE rolid = 2) u4,
        (SELECT 
            COUNT(texid) AS texnum,
            SUM(1 - texestado) AS texnum_inactivos
        FROM academico.texto) t;
    ''')  

def listarCursoMateriaContabilidad(data):
    print("params", data)
    fecini = darFormatoFechaSinHorav2(data['fecini'])
    fecfin = darFormatoFechaSinHorav2(data['fecfin'])
    print("fecini", fecini)
    print("fecfin", fecfin)
    lista_cm = select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, p.perfoto, cm.curmatfecini, cm.curmatfecfin, cm.curmatcosto, t1.numest as numero_estudiantes
        FROM academico.curso_materia cm
        JOIN ( SELECT curmatid, count(peridestudiante) as numest FROM academico.inscripcion WHERE insestado = 1 GROUP BY curmatid) as t1 ON t1.curmatid = cm.curmatid
        LEFT JOIN academico.curso c ON c.curid = cm.curid
        LEFT JOIN academico.materia m ON m.matid = cm.matid
        LEFT JOIN academico.persona p on p.perid = cm.periddocente
        WHERE cm.curmatfecini > '{fecini}' AND cm.curmatfecfin < '{fecfin}'
        and cm.curmatestado = 1
    ''')
    for lcm in lista_cm:
        lcm['curmatfecini'] = darFormatoFechaSinHora(lcm['curmatfecini'])
        lcm['curmatfecfin'] = darFormatoFechaSinHora(lcm['curmatfecfin'])
    print("listarCursoMateriaContabilidad: ", lista_cm)
    return lista_cm

def gestionarPago(data):
    data = {key: f'\'{value}\'' if value is not None else 'NULL' for key, value in data.items()}

    return execute_function(f'''
       SELECT academico.f_gestionar_pago_2  
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
    
# Insertar pago
def insertarPago(data):
    # print("Data_insertarPago: ", data)
    res = execute_function(f'''
       SELECT academico.f_pago_insertar (  
                \'{data['pagdescripcion']}\', 
                {data['pagmonto']}, 
                \'{data['pagfecha']}\',
                \'{data['pagarchivo']}\',
                \'{data['pagusureg']}\',
                {data['pagtipo']}
                ) as valor;
    ''')
    # print("insertarPago: ", res)
    return res

# Modificar pago
def modificarPago(data):
    # print("DatamodificarPago: ", data)
    res = execute_function(f'''
       SELECT academico.f_pago_modificar (  
                  {data['pagid']}, 
                \'{data['pagdescripcion']}\', 
                  {data['pagmonto']}, 
                \'{data['pagarchivo']}\',
                \'{data['pagusumod']}\',
                \'{data['pagfecha']}\',
                  {data['pagtipo']},
                  {data['archivobol']}
                ) as valor;
    ''')
    # print("modificarPago: ", res)
    return res

# Asignar pago a inscripcion
def asignarPagoInscripcion(data):
    # print("asignarPagoInscripcion: ", data)
    res = execute_function(f'''
       SELECT academico.f_pago_asignar_a_inscripcion (  
                {data['insid']}, 
                {data['pagid']}, 
                \'{data['pagusumod']}\'
                ) as valor;
    ''')
    # print("asignarPagoInscripcion2: ", res)
    return res


def obtenerUltimoPago():
    return select(f'''
       select pagid from academico.pago p where pagestado = 1 order by pagid desc limit 1
    ''') 
    
# def listarPagoEstudiante(data):
#     return select(f'''
#         SELECT i.insid, i.matrid, cm.curid, c.curnombre, cm.matid, m.matnombre, i.peridestudiante, i.pagid, i.insusureg, i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion 
#         FROM academico.inscripcion i
#         left join academico.curso_materia cm on cm.curmatid = i.curmatid
#         left join academico.curso c on c.curid = cm.curid
#         left join academico.materia m on m.matid = cm.matid
#         where i.peridestudiante = {data['perid']}
#         order by c.curnombre, m.matnombre; 
#     ''') 

def listarPagoEstudiante(data):
    lista_pago_estudiante = select(f'''
         select distinct i.insid, i.matrid, cm.curid, 
               c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, i.peridestudiante, i.pagid, i.insusureg,
               i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion 
            
          FROM academico.inscripcion i
          left join academico.curso_materia cm on cm.curmatid = i.curmatid
          left join academico.curso c on c.curid = cm.curid
          left join academico.materia m on m.matid = cm.matid
          LEFT JOIN academico.persona p ON p.perid = cm.periddocente
          where i.peridestudiante = {data['perid']}
          order by c.curnombre, m.matnombre; 
    ''')

    for pago_estudiante in lista_pago_estudiante:
        pago_estudiante["insfecreg"] = darFormatoFechaConHora(pago_estudiante["insfecreg"])
        pago_estudiante["insfecmod"] = darFormatoFechaConHora(pago_estudiante["insfecmod"])
        pago_estudiante["curmatfecini"] = darFormatoFechaSinHora(pago_estudiante["curmatfecini"])
        pago_estudiante["curmatfecfin"] = darFormatoFechaSinHora(pago_estudiante["curmatfecfin"])

    return lista_pago_estudiante


def listarPagoEstudianteMateria(data):
    return select(f'''
       SELECT distinct 
                i.insid, i.matrid, m.matrgestion, i.curmatid, c.curnombre, m2.matnombre, i.peridestudiante, p2.perfoto,
                i.pagid, p.pagdescripcion, p.pagmonto, p.pagarchivo, pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagtipo, pagfecha
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.pago p on p.pagid = i.pagid
        left join academico.persona p2 on p2.perid = i.peridestudiante
        where i.peridestudiante = {data['perid']}
        and cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
    ''') 

def listarPagoCurso():
    lista = select(f'''
        SELECT distinct cm.curmatid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, p.perfoto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        order by c.curnombre, m.matnombre;
    ''')  
    for pago in lista:
        pago["curmatfecreg"] = darFormatoFechaConHora(pago["curmatfecreg"])
        pago["curmatfecmod"] = darFormatoFechaConHora(pago["curmatfecmod"])
        pago["curmatfecini"] = darFormatoFechaSinHora(pago["curmatfecini"])
        pago["curmatfecfin"] = darFormatoFechaSinHora(pago["curmatfecfin"]) 
    return lista
    
# Listar los pagos de los estudiantes por materia filtrado por curso y materia.
def listarPagoEstudiantesMateria(data):
    lista = select(f'''
       SELECT distinct 
            i.insid, i.matrid, i.curmatid, i.peridestudiante, i.pagid,
            m.matrgestion, 
            c.curnombre, 
            m2.matnombre, 
            p2.pernomcompleto,
            p2.perfoto,
            p.pagfecha, p.pagdescripcion, p.pagmonto, p.pagarchivo, 
            pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagtipo 
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
    # print("listarPagoEstudiantesMateria: ", lista)
    for pago in lista:
        pago["pagfecreg"] = darFormatoFechaConHora(pago["pagfecreg"])
        pago["pagfecmod"] = darFormatoFechaConHora(pago["pagfecmod"])
        pago["pagfecha"] = darFormatoFechaConHora(pago["pagfecha"])
    print(lista)
    return lista 
    
def tipoPago():
    return select(f'''
   select tp.tpagid, tp.tpagnombre from academico.tipo_pago tp              
    ''')    