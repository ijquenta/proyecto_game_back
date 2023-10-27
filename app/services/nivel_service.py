from core.database import select, as_string, execute, execute_function
from psycopg2 import sql

def listarNivel():
    return select(f'''
    SELECT curid, curnombre, curdescripcion, curestadodescripcion, curnivel, curdesnivel, curfchini, curfchfin, curusureg, curfecreg, curusumod, curfecmod, curestado
    FROM academico.curso
    order by curestado desc;
    ''')

def registrarDeduccionDocente(data,user):
    return execute_function(f'''
    select p_bsocial.bs_registrar_deduccion({data['ano']}, {data['mes']}, \'{data['codDocente']}\', \'{data['nroLiquidacion']}\', \'{data['designacion']}\', {data['codTipoDeduccion']}, {data['montoDeduccion']}, \'{data['observaciones']}\', \'{user}\') as valor;
''')    

def insertarNivel(data):
    print("Insertar Nivel: ", data)
    return execute_function(f'''
    SELECT academico.insertar_curso(\'{data['curnombre']}\', {data['curestado']}, \'{data['curestadodescripcion']}\', {data['curnivel']},  \'{data['curfchini']}\',  \'{data['curfchfin']}\', \'{data['curusureg']}\', \'{data['curusumod']}\', \'{data['curdesnivel']}\', \'{data['curdescripcion']}\')  as valor;                      
    ''')
    
def eliminarNivel(data):
    print("Eliminar Nivel: ", data)
    return execute_function(f'''
    SELECT eliminar_curso({data['curid']}) as valor;
    ''')
    

