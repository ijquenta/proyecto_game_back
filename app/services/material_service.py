from core.database import select, execute, execute_function, execute_response


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