from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from utils.date_formatting import *

def listarNivel():
    lista_niveles = select(f'''
    SELECT curid, curnombre, curdescripcion, curestadodescripcion, curnivel, curdesnivel, curfchini, curfchfin, curusureg, curfecreg, curusumod, curfecmod, curestado
    FROM academico.curso
    order by curid desc;
    ''')
    for nivel in lista_niveles:
        nivel["curfchini"] = darFormatoFechaSinHora(nivel["curfchini"])
        nivel["curfchfin"] = darFormatoFechaSinHora(nivel["curfchfin"])
        nivel["curfecreg"] = darFormatoFechaConHora(nivel["curfecreg"])
        nivel["curfecmod"] = darFormatoFechaConHora(nivel["curfecmod"])
    return lista_niveles


def insertarNivel(data):
    return execute_function(f'''
    SELECT academico.insertar_curso(
        \'{data['curnombre']}\', 
          {data['curestado']}, 
        \'{data['curestadodescripcion']}\', 
          {data['curnivel']},
        \'{data['curfchini']}\',  
        \'{data['curfchfin']}\', 
        \'{data['curusureg']}\', 
        \'{data['curusumod']}\', 
        \'{data['curdesnivel']}\', 
        \'{data['curdescripcion']}\')  as valor;                      
    ''')
    
    
def modificarNivel(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.modificar_curso({curid}, {curnombre}, {curnivel}, {curdesnivel}, {curdescripcion}, {curfchini}, {curfchfin}, {curestado}, {curestadodescripcion}, {curusumod});
            ''').format(
                curid=sql.Literal(data['curid']),
                curnombre=sql.Literal(data['curnombre']),
                curnivel=sql.Literal(data['curnivel']),
                curdesnivel=sql.Literal(data['curdesnivel']),
                curdescripcion=sql.Literal(data['curdescripcion']),
                curfchini=sql.Literal(data['curfchini']),
                curfchfin=sql.Literal(data['curfchfin']),
                curestado=sql.Literal(data['curestado']),
                curestadodescripcion=sql.Literal(data['curestadodescripcion']),
                curusumod=sql.Literal(data['curusumod'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result
 
    
def eliminarNivel(data):
    resultado = execute_function(f'''
    SELECT academico.eliminar_curso({data['curid']}) as valor;
    ''')
    result = resultado[0]['valor']
    if result == 1:
        response_data = {'message': 'Nivel eliminado correctamente'}
        status_code = 200
    else:
        if result == 0:
            response_data = {'message': 'No se pudo eliminar el nivel'}
            status_code = 500
        else:
            response_data = {'message': 'No se puede eliminar el curso debido a que tiene registros relacionados'}
            status_code = 500
        print("response_data: ",response_data)    

    return make_response(jsonify(response_data), status_code)

def gestionarNivelEstado(data):
    return execute_function(f'''
    SELECT academico.f_nivel_gestionar_estado(
          {data['tipo']}, 
          {data['curid']}, 
        \'{data['curusumod']}\'
        )  as valor;                      
    ''')