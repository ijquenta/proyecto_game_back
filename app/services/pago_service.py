from core.database import select, execute_function
from flask import jsonify, make_response
from utils.date_formatting import *
from models.pago import modelPago



def listarPago():
    return select('''
        SELECT pagid, pagdescripcion, pagmonto, pagarchivo, pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagfecha, pagtipo FROM academico.pago WHERE pagestado = 1;
    ''')

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
    
def insertarPago(data):
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
    return res

def modificarPago(data):
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
    return res

def asignarPagoInscripcion(data):
    res = execute_function(f'''
       SELECT academico.f_pago_asignar_a_inscripcion (  
                {data['insid']}, 
                {data['pagid']}, 
                \'{data['pagusumod']}\'
                ) as valor;
    ''')
    return res

def asignarPagoMatricula(data):
    res = execute_function(f'''
       SELECT academico.f_pago_asignar_a_matricula (  
                {data['matrid']}, 
                {data['pagid']}, 
                \'{data['matrusumod']}\'
                ) as valor;
    ''')
    return res


def obtenerUltimoPago():
    return select(f'''
       select pagid from academico.pago p where pagestado = 1 order by pagid desc limit 1
    ''') 
    
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
                i.insid, i.matrid, tm.tipmatrgestion, i.curmatid, c.curnombre, m2.matnombre, i.peridestudiante, p2.perfoto,
                i.pagid, p.pagdescripcion, p.pagmonto, p.pagarchivo, pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagtipo, pagfecha
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
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
    
def listarPagoEstudiantesMateria(data):
    lista = select(f'''
        SELECT distinct i.insid, i.curmatid, i.peridestudiante, 
                    i.pagid, m.matrid, tm.tipmatrgestion, c.curnombre, m2.matnombre, p2.pernomcompleto, 
                    p2.perfoto, p.pagfecha, p.pagdescripcion, p.pagmonto, p.pagarchivo, 
                    pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagtipo 
        FROM academico.inscripcion i 
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.tipo_matricula tm on m.tipmatrid = tm.tipmatrid
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.pago p on p.pagid = i.pagid 
        left join academico.persona p2 on p2.perid = i.peridestudiante 
        where cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
    ''')
    for pago in lista:
        pago["pagfecreg"] = darFormatoFechaConHora(pago["pagfecreg"])
        pago["pagfecmod"] = darFormatoFechaConHora(pago["pagfecmod"])
        pago["pagfecha"] = darFormatoFechaConHora(pago["pagfecha"])
    return lista 
    
def tipoPago():
    return select(f'''
   select tp.tpagid, tp.tpagnombre from academico.tipo_pago tp              
    ''')    

def getPayments():
    pagos = modelPago.query.all()
    pagos_json = [pago.to_dict() for pago in pagos]
    return make_response(jsonify(pagos_json), 200)