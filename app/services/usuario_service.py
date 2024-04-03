from core.database import select, execute, execute_function, as_string
from psycopg2 import sql
from werkzeug.security import generate_password_hash, check_password_hash

def gestionarUsuario(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_gestionar_usuario({tipo}, {usuid}, {perid}, {rolid}, {usuname}, {usupassword}, {usupasswordhash}, {usuemail}, {usuimagen}, {usudescripcion}, {usuestado}, {usuusureg});
            ''').format( tipo=sql.Literal(data['tipo']), usuid=sql.Literal(data['usuid']), perid=sql.Literal(data['perid']), rolid=sql.Literal(data['rolid']), usuname=sql.Literal(data['usuname']), usupassword = sql.Literal(generate_password_hash(data['usupassword'])), usupasswordhash= sql.Literal(generate_password_hash(data['usupassword'])), usuemail=sql.Literal(data['usuemail']), usuimagen=sql.Literal(data['usuimagen']), usudescripcion=sql.Literal(data['usudescripcion']), usuestado=sql.Literal(data['usuestado']), usuusureg=sql.Literal(data['usuusureg']))
        result = execute(as_string(query))
    except Exception as err:
        print("Error en Gestionar Usuario: ",err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def listaUsuario():
    return select(f'''
        SELECT 
        u.usuid, u.perid, p.pernomcompleto, p.pernrodoc, p.perfoto, u.rolid, r.rolnombre, u.usuname, 
        u.usuemail, u.usudescripcion, 
        u.usuestado, u.usuusureg, u.usufecreg, u.usuusumod, u.usufecmod
        FROM academico.usuario u
        inner join academico.persona p on p.perid = u.perid
        inner join academico.rol r on r.rolid = u.rolid 
        order by p.pernomcompleto 
    ''')
    
def tipoPersona():
    return select(f''' 
    select perid, pernomcompleto, pernrodoc, perfoto from academico.persona p 
    order by pernomcompleto 
    ''')

def perfil(data):
    return select(f'''
    SELECT u.usuid, u.perid, p.pernomcompleto, u.rolid, r.rolnombre , u.usuname, u.usuemail, u.usuimagen 
    FROM academico.usuario u
    left join academico.persona p on p.perid = u.perid
    left join academico.rol r on r.rolid = u.rolid 
    where u.usuid ={data['usuid']};
    ''')

def listarRoles():
    return select(f'''
    SELECT rolid, rolnombre, roldescripcion, rolusureg, rolfecreg, rolusumod, rolfecmod, rolestado
    FROM academico.rol
    where rolestado = 1
    order by rolid;        
    ''')
    
def crearRol(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT * from academico.agregarrol({rolNombre}, {rolDescripcion}, {rolUsuReg});
            ''').format( rolNombre=sql.Literal(data['rolNombre']), rolDescripcion=sql.Literal(data['rolDescripcion']), rolUsuReg=sql.Literal(data['rolUsuReg']))
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def modificarRol(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.modificarrol2({rolId}, {rolNombre}, {rolDescripcion}, {rolUsuMod});
            ''').format( rolId=sql.Literal(data['rolId']), rolNombre=sql.Literal(data['rolNombre']), rolDescripcion=sql.Literal(data['rolDescripcion']), rolUsuMod=sql.Literal(data['rolUsuMod']))
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def eliminarRol(data):
    print("Datos eliminar->",data)
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.eliminarRol2({rolid}, {rolusumod});
            ''').format(rolid=sql.Literal(data['rolid']),rolusumod=sql.Literal(data['rolusumod']))
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def listarUsuarios():
    return select(f'''
    SELECT id, nombre_usuario, contrasena, nombre_completo, rol
    FROM public.usuarios;
    ''')

def eliminarRol2(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            select * from f_rol_eliminar({rolId});
            ''').format(
                rolId=sql.Literal(data['rolId'])
            )
        print("Consulta SQL:", query, data['rolId'])
        result = execute(as_string(query))
        print(result)
    except Exception as err:
        print("Error:", err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

# def listarPersona():
#     listPersons = select(f'''
#      SELECT p.perid, p.pernomcompleto, p.pernombres, p.perapepat, p.perapemat, 
#         p.pertipodoc, td.tipodocnombre, 
#         p.pernrodoc, p.perfecnac, p.perdirec, p.peremail, p.percelular, p.pertelefono, 
#         p.perpais, tp.paisnombre, 
#         p.perciudad, tc.ciudadnombre,
#         p.pergenero, tg.generonombre,
#         p.perestcivil, te.estadocivilnombre,
#         p.perfoto, p.perestado, p.perobservacion, p.perusureg, p.perfecreg, p.perusumod, p.perfecmod 
#         FROM academico.persona p
#         left join academico.tipo_documento td on td.tipodocid = p.pertipodoc
#         left join academico.tipo_pais tp on tp.paisid = p.perpais
#         left join academico.tipo_ciudad tc on tc.ciudadid = p.perciudad
#         left join academico.tipo_genero tg on tg.generoid = p.pergenero
#         left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil    
#         ORDER BY p.perid desc; 
#     ''')
#     print(listPersons)
#     return listPersons
from datetime import datetime

def darFormatoFecha(fecha_str):
    if fecha_str is None:
       return None
    # Convertir la cadena de fecha a un objeto datetime
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Formatear la fecha como desees, por ejemplo, "DD/MM/AAAA HH:MM:SS"
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y %H:%M:%S")

    return fecha_formateada

def darFormatoFechaNacimiento(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
    return fecha_formateada

def listarPersona():
    listPersons = select('''
     SELECT p.perid, p.pernomcompleto, p.pernombres, p.perapepat, p.perapemat, 
        p.pertipodoc, td.tipodocnombre, 
        p.pernrodoc, p.perfecnac, p.perdirec, p.peremail, p.percelular, p.pertelefono, 
        p.perpais, tp.paisnombre, 
        p.perciudad, tc.ciudadnombre,
        p.pergenero, tg.generonombre,
        p.perestcivil, te.estadocivilnombre,
        p.perfoto, p.perestado, p.perobservacion, p.perusureg, p.perfecreg, p.perusumod, p.perfecmod 
        FROM academico.persona p
        left join academico.tipo_documento td on td.tipodocid = p.pertipodoc
        left join academico.tipo_pais tp on tp.paisid = p.perpais
        left join academico.tipo_ciudad tc on tc.ciudadid = p.perciudad
        left join academico.tipo_genero tg on tg.generoid = p.pergenero
        left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil    
        ORDER BY p.perid desc; 
    ''')

    for person in listPersons:
        person["perfecnac"] = darFormatoFechaNacimiento(person["perfecnac"])
        person["perfecreg"] = darFormatoFecha(person["perfecreg"])
        person["perfecmod"] = darFormatoFecha(person["perfecmod"])

    return listPersons

# Ejemplo de uso
personas_formateadas = listarPersona()
# print(personas_formateadas)




def obtenerEmail(data):
    res = select(f'''
    select usuid, usuname, usuemail from academico.usuario u where usuname = \'{data['usuname']}\' and usuemail = \'{data['usuemail']}\'
    ''')
    print ("res: ", res)
    return res

