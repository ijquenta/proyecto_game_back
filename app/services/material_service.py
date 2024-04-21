from core.database import select, execute, execute_function, execute_response, execute_function_multiple
from utils.date_formatting import darFormatoFechaConHora

def listarMaterial():
    return select('''
        SELECT mt.mattexid, mt.matid, m.matnombre, mt.texid, t.texnombre, t.textipo, t.texdocumento, t.texusureg, t.texfecreg, t.texusumod, t.texfecmod, t.texestado 
        FROM academico.materia_texto mt
        inner join academico.texto t on t.texid = mt.texid 
        inner join academico.materia m on m.matid = mt.matid 
    ''')


def listarTexto():
    return select('''
        SELECT texid, texnombre, textipo, texdocumento, texusureg, texfecreg, texusumod, texfecmod, texestado FROM academico.texto order by texid desc;
    ''')
    
# Insertar texto
def insertarTexto(data):
    # print("Data_insertarTexto: ", data)
    res = execute_function(f'''
       SELECT academico.f_texto_insertar (  
                \'{data['texnombre']}\', 
                \'{data['textipo']}\', 
                \'{data['texdocumento']}\',
                \'{data['texusureg']}\'
                ) as valor;
    ''')
    # print("insertarTexto: ", res)
    return res



def listarMateriaTexto():
    lista_materia_texto = select(f'''
        SELECT distinct mt.mattexid, mt.matid, m.matnombre, mt.texid, t.texnombre, t.textipo, t.texdocumento, mattexdescripcion, mt.mattexusureg, mt.mattexfecreg, mt.mattexusumod, mt.mattexfecmod, mt.mattexestado  
        FROM academico.materia_texto mt
        left join academico.materia m on m.matid = mt.matid 
        left join academico.texto t on t.texid = mt.texid
        order by m.matnombre 
    ''')
    for materia_texto in lista_materia_texto:
        materia_texto["mattexfecreg"] = darFormatoFechaConHora(materia_texto["mattexfecreg"])
        materia_texto["mattexfecmod"] = darFormatoFechaConHora(materia_texto["mattexfecmod"])
    return lista_materia_texto
    
    
    
    
def listarTextoCombo():
    return select(f'''
        select distinct t.texid, t.texnombre 
        from academico.texto t
        where t.texestado = 1
        order by t.texnombre       
        ''')
    
    
def insertarMateriaTexto(data):
    res = execute_function(f'''
       SELECT academico.f_materia_texto_insertar (  
                {data['matid']}, 
                {data['texid']}, 
                \'{data['mattexdescripcion']}\',
                \'{data['mattexusureg']}\'
                ) as valor;
    ''')
    return res

def modificarMateriaTexto(data):
    query = f'''
       SELECT academico.f_materia_texto_modificar (  
                {data['mattexid']},
                {data['matid']}, 
                {data['texid']}, 
                \'{data['mattexdescripcion']}\',
                \'{data['mattexusumod']}\'
                );
    '''
    res = execute_function(query)
    return res
