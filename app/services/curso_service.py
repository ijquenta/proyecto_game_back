from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response

def listarCursoMateria():
    return select(f'''
    SELECT curmatid, c.curnombre , cm.curid, m.matnombre, cm.matid, m.matnivel, p.pernombrecompleto, p.pernombres, p.perapepat, p.perapemat, cm.periddocente, curmatfecini, curmatfecfin, curmatestado, curmatestadodescripcion, curmatusureg, curmatfecreg, curmatusumod, curmatfecmod, curmatidrol, curmatidroldes
    FROM academico.curso_materia cm
    inner join academico.curso c on c.curid  = cm.curid 
    inner join academico.materia m on m.matid = cm.matid 
    inner join academico.persona p on p.perid = cm.periddocente 
    order by curmatid desc;       
    ''')
    
def eliminarCursoMateria(data):
    return execute_function(f'''
    SELECT academico.eliminar_curso_materia({data['curmatid']});
    ''')

def eliminarCursoMateria(data):
    resultado = execute_function(f'''
    SELECT academico.eliminar_curso_materia({data['curmatid']}) as valor;
    ''')
    result = resultado[0]['valor']
    print("Resultado: ", result)
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
        print("response_data: ",response_data)    

    return make_response(jsonify(response_data), status_code)

def insertarCursoMateria(data):
    print("Datos para insertar a CursoMateria", data)
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
                        SELECT academico.insertar_curso_materia
                        ({curid}, {matid}, {perid}, {fecini}, {fecfin}, {estado}, {estadodes}, {usureg}, {idrol}, {idroldes});''').format(
                            curid = sql.Literal(data['curid']),
                            matid = sql.Literal(data['matid']),
                            perid = sql.Literal(data['periddocente']),
                            fecini = sql.Literal(data['curmatfecini']),
                            fecfin = sql.Literal(data['curmatfecfin']),
                            estado = sql.Literal(data['curmatestado']),
                            estadodes = sql.Literal(data['curmatestadodescripcion']),
                            usureg = sql.Literal(data['curmatusureg']),
                            idrol = sql.Literal(data['curmatidrol']),
                            idroldes = sql.Literal(data['curmatidroldes'])
                         )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def modificarCursoMateria(data):
    print("Datos para modificar de CursoMateria: ", data)
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
                                    \'{data['curmatidroldes']}\'
                                ) as valor;
                                 ''')
    print("Resuldato modificarCursoMateria: ", resultado)
    return resultado


def listaCursoCombo():
    return select(f'''
    SELECT curid, curnombre, curnivel
    FROM academico.curso
    where curestadodescripcion = 'VIGENTE'
    order by curnivel      
    ''')

def listaPersonaDocenteCombo(data):
    return select(f'''
    select pe.perid, pe.pernombrecompleto
    from academico.persona pe 
    inner join academico.roles r ON r.rolid = pe.peridrol
    where r.rolnombre = \'{data['rolnombre']}\'  
    ''')
    
def tipoRol():
    return select(f'''
    SELECT rolid, rolnombre
	FROM academico.rol
	--listarPersona where rolid != 1
	order by rolnombre;                
    ''')