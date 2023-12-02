from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response

# def extractDate(isoFecha):
#     if isoFecha is None:
#         return None
#     return datetime.fromisoformat(isoFecha[:-1] + '+00:00').strftime('%d-%m-%Y')

def listarMatricula():
    return select(f'''
    SELECT matrid, matrgestion, matrestadodescripcion, matrfchini, matrfchfin, matrcos, matrusureg, matrfecreg, matrusumod, matrfecmod, matrestado
    FROM academico.matricula
    order by matrid desc;
    ''')


def insertarMatricula(data):
    print("Insertar Matricula: ", data)
    return execute_function(f'''
    SELECT academico.insertar_matricula(
        \'{data['matrgestion']}\', 
        \'{data['matrestadodescripcion']}\', 
        \'{data['matrfchini']}\', 
        \'{data['matrfchfin']}\',
          {data['matrcos']},  
          {data['matrestado']}, 
        \'{data['matrusureg']}\')  as valor;                      
    ''')
def modificarMatricula(data):
    print("Modificar Matricula: ", data)
    return execute_function(f'''
    SELECT academico.modificar_matricula(
          {data['matrid']}, 
        \'{data['matrgestion']}\', 
        \'{data['matrestadodescripcion']}\', 
        \'{data['matrfchini']}\', 
        \'{data['matrfchfin']}\',
          {data['matrcos']},  
          {data['matrestado']}, 
        \'{data['matrusumod']}\')  as valor;                      
    ''')  

def eliminarMatricula(data):
    print("Eliminar Matricula: ", data)
    return execute_function(f'''
    SELECT academico.eliminar_matricula(
        \'{data['matrid']}\')  as valor;                      
    ''')  
