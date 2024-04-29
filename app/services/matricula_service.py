from core.database import select, execute_function
from utils.date_formatting import *

def listarMatricula():
    lista = select(f'''
        SELECT m.matrid, m.matrfec,
            m.tipmatrid, tm.tipmatrgestion, tm.tipmatrfecini, tm.tipmatrfecfin, tm.tipmatrcosto, 
            m.peridestudiante, p.pernomcompleto, p.pernrodoc, p.perfoto,
            m.pagoidmatricula, p2.pagdescripcion, p2.pagmonto, p2.pagarchivo, p2.pagfecha, p2.pagtipo,
            m.matrusureg, m.matrfecreg, m.matrusumod, m.matrfecmod, m.matrestado, m.matrdescripcion 
        FROM academico.matricula m
        LEFT JOIN 
            academico.persona p ON p.perid = m.peridestudiante
        LEFT JOIN 
            academico.pago p2 ON p2.pagid = m.pagoidmatricula
        LEFT JOIN 
            academico.tipo_matricula tm ON tm.tipmatrid = m.tipmatrid
    ''')
    for l in lista:
        l['tipmatrfecini'] = darFormatoFechaSinHora(l['tipmatrfecini'])
        l['tipmatrfecfin'] = darFormatoFechaSinHora(l['tipmatrfecfin'])
        l['matrfec'] = darFormatoFechaSinHora(l['matrfec']) 
        l['matrfecreg'] = darFormatoFechaConHora(l['matrfecreg'])
        l['matrfecmod'] = darFormatoFechaConHora(l['matrfecmod'])
        l['pagfecha'] = darFormatoFechaSinHora(l['pagfecha'])
    return lista

def insertarMatricula(data):
    return execute_function(f'''
    SELECT academico.f_matricula_insertar(
          {data['tipmatrid']},
        \'{data['matrfec']}\',
          {data['peridestudiante']},
          NULL,
        \'{data['matrusureg']}\',
        \'{data['matrdescripcion']}\')  as valor;    
                            ''')
def modificarMatricula(data):
    return execute_function(f'''
    SELECT academico.f_matricula_modificar(
          {data['matrid']},
          {data['tipmatrid']},
        \'{data['matrfec']}\',
          {data['peridestudiante']},
        \'{data['matrusumod']}\',
        \'{data['matrdescripcion']}\')  as valor;
    ''')   

def gestionarMatriculaEstado(data):
    return execute_function(f'''
    SELECT academico.f_matricula_gestionar_estado(
          {data['tipo']}, 
          {data['matrid']}, 
        \'{data['matrusumod']}\')  as valor;                      
    ''')  

def listarTipoMatricula():
    lista = select(f''' 
                  SELECT tipmatrid, tipmatrgestion, tipmatrfecini, tipmatrfecfin, 
                         tipmatrcosto, tipmatrusureg, tipmatrfecreg, tipmatrusumod,
                         tipmatrfecmod, tipmatrestado, tipmatrdescripcion 
                  FROM academico.tipo_matricula 
                  --    WHERE tipmatrestado = 1
                  ORDER BY tipmatrid;
                  ''')
    for l in lista:
        l['tipmatrfecini'] = darFormatoFechaSinHora(l['tipmatrfecini'])
        l['tipmatrfecfin'] = darFormatoFechaSinHora(l['tipmatrfecfin'])
        l['tipmatrfecreg'] = darFormatoFechaConHora(l['tipmatrfecreg'])
        l['tipmatrfecmod'] = darFormatoFechaConHora(l['tipmatrfecmod'])
    return lista

def listarTipoMatriculaCombo():
    lista = select(f'''
        SELECT tipmatrid, tipmatrgestion
        FROM academico.tipo_matricula
        WHERE tipmatrestado = 1
        ORDER BY tipmatrgestion;
        ''')
    return lista

def listarTipoPersonaEstudiante():
    return select(f'''          
        select u.perid, p.pernomcompleto, p.perfoto 
        from academico.usuario u
        left join academico.persona p on p.perid = u.perid 
        where u.rolid = 4
        and p.perestado = 1
        and u.usuestado = 1
        order by p.pernomcompleto;
    ''')
















# otras funciones 

def eliminarMatricula(data):
    return execute_function(f'''
    SELECT academico.eliminar_matricula(
        \'{data['matrid']}\')  as valor;                      
    ''')  



def insertarTipoMatricula(data):
    return execute_function(f'''
    SELECT academico.f_tipo_matricula_insertar(
        \'{data['tipmatrgestion']}\',
        \'{data['tipmatrfecini']}\',
        \'{data['tipmatrfecfin']}\',
        {data['tipmatrcosto']},
        \'{data['tipmatrusureg']}\',
        \'{data['tipmatrdescripcion']}\')  as valor;
    ''')
    
def modificarTipoMatricula(data):
    return execute_function(f'''
    SELECT academico.f_tipo_matricula_modificar(
        {data['tipmatrid']},
        \'{data['tipmatrgestion']}\',
        \'{data['tipmatrfecini']}\',
        \'{data['tipmatrfecfin']}\',
        {data['tipmatrcosto']},
        \'{data['tipmatrusumod']}\',
        \'{data['tipmatrdescripcion']}\')  as valor;
    ''')    
    
def gestionarTipoMatriculaEstado(data):
    return execute_function(f'''
    SELECT academico.f_tipo_matricula_gestionar_estado(
        {data['tipo']},
        {data['tipmatrid']},
        \'{data['tipmatrusumod']}\')  as valor;
    ''')