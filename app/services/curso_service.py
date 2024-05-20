from core.database import select, as_string, execute, execute_function, execute_response
from psycopg2 import sql
from flask import jsonify, make_response
from utils.date_formatting import *

def listarCursoMateria():
    lista_cursos = select(f'''
        SELECT distinct cm.curmatid, c.curnombre, cm.curid, m.matnombre, cm.matid, m.matnivel, 
        p.pernomcompleto, p.perfoto, p.pernrodoc, p.pernombres, p.perapepat, p.perapemat, cm.periddocente, 
        c.curnivel,
        cm.curmatfecini, cm.curmatfecfin, cm.curmatestado, cm.curmatestadodescripcion, 
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatidrol as rolid, cm.curmatidroldes as rolnombre, cm.curmatcosto
        FROM academico.curso_materia cm
        inner join academico.curso c on c.curid  = cm.curid 
        inner join academico.materia m on m.matid = cm.matid 
        inner join academico.persona p on p.perid = cm.periddocente 
        inner join academico.usuario u on u.perid = cm.periddocente
        inner join academico.rol r on r.rolid = u.rolid
        order by curmatid desc;      
        ''')
    for curso in lista_cursos:
        curso["curmatfecini"] = darFormatoFechaSinHora(curso["curmatfecini"])
        curso["curmatfecfin"] = darFormatoFechaSinHora(curso["curmatfecfin"])
        curso["curmatfecreg"] = darFormatoFechaConHora(curso["curmatfecreg"])
        curso["curmatfecmod"] = darFormatoFechaConHora(curso["curmatfecmod"])
    return lista_cursos
    
def eliminarCursoMateria(data):
    resultado = execute_function(f'''
    SELECT academico.eliminar_curso_materia({data['curmatid']}) as valor;
    ''')
    result = resultado[0]['valor']
    if result == 1:
        response_data = {'message': 'Curso Materia eliminado correctamente'}
        status_code = 200
    else:
        if result == 0:
            response_data = {'message': 'No se pudo eliminar el curso materia'}
            status_code = 500
        else:
            response_data = {'message': 'No se puede eliminar la curso materia debido a que tiene registros relacionados'}
            status_code = 500
    return make_response(jsonify(response_data), status_code)

def insertarCursoMateria(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL(''' SELECT academico.insertar_curso_materia ({curid}, {matid}, {perid}, {fecini}, {fecfin}, {estado}, {estadodes}, {usureg}, {idrol}, {idroldes}, {costo});''').format( curid = sql.Literal(data['curid']), matid = sql.Literal(data['matid']), perid = sql.Literal(data['periddocente']), fecini = sql.Literal(data['curmatfecini']), fecfin = sql.Literal(data['curmatfecfin']), estado = sql.Literal(data['curmatestado']), estadodes = sql.Literal(data['curmatestadodescripcion']), usureg = sql.Literal(data['curmatusureg']), idrol = sql.Literal(data['curmatidrol']), idroldes = sql.Literal(data['curmatidroldes']), costo = sql.Literal(data['curmatcosto']) )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def modificarCursoMateria(data):
    # print("Data original: ", data)
    data['curmatfecini'] = volverAFormatoOriginal(data['curmatfecini']) 
    data['curmatfecfin'] = volverAFormatoOriginal(data['curmatfecfin']) 
    # print("Fechas modificadas: ", data)
    resultado = execute_function(f'''
        SELECT academico.modificar_curso_materia(
              {data['curmatid']},
              {data['curid']},
              {data['matid']},
              {data['periddocente']},
            \'{data['curmatfecini']}\',
            \'{data['curmatfecfin']}\',
              {data['curmatestado']},
            \'{data['curmatestadodescripcion']}\',
            \'{data['curmatusumod']}\',
            \'{data['curmatidrol']}\',
            \'{data['curmatidroldes']}\',
              {data['curmatcosto']}
        ) as valor;
         ''')
    return resultado


def listaCursoCombo():
    return select(f'''
    SELECT curid, curnombre, curnivel
    FROM academico.curso
    where curestado = 1
    order by curnivel      
    ''')

def listaPersonaDocenteCombo(data):
    return select(f'''
    select distinct p.perid, p.pernomcompleto, p.perfoto, p.pernrodoc
    from academico.persona p 
    inner join academico.usuario u on u.perid = p.perid
    inner join academico.rol r ON r.rolid = u.rolid
    where r.rolnombre = \'{data['rolnombre']}\'
    and p.perestado = 1
    order by p.pernomcompleto  
    ''')
    
def tipoRol():
    return select(f'''
    SELECT rolid, rolnombre
	FROM academico.rol
	order by rolnombre;                
    ''')
    
    
def gestionarCursoMateriaEstado(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
                        SELECT academico.f_curso_materia_gestionar_estado
                        ({tipo}, {curmatid}, {curmatusumod});''').format(
                            tipo = sql.Literal(data['tipo']),
                            curmatid = sql.Literal(data['curmatid']),
                            curmatusumod = sql.Literal(data['curmatusumod'])
                        )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result