# Importamos librerias
from psycopg2 import sql 
from utils.date_formatting import *
from core.database import select, execute, as_string
from werkzeug.security import generate_password_hash

# Gestionar Usuario
def gestionarUsuario(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_gestionar_usuario(
                        {tipo}, {usuid}, {perid}, {rolid}, {usuname}, {usupassword}, {usupasswordhash}, 
                        {usuemail}, {usudescripcion}, {usuestado}, {usuusureg});
            ''').format( tipo=sql.Literal(data['tipo']), 
                         usuid=sql.Literal(data['usuid']), 
                         perid=sql.Literal(data['perid']), 
                         rolid=sql.Literal(data['rolid']), 
                         usuname=sql.Literal(data['usuname']), 
                         usupassword = sql.Literal(generate_password_hash(data['usupassword'])),
                         usupasswordhash= sql.Literal(generate_password_hash(data['usupassword'])), 
                         usuemail=sql.Literal(data['usuemail']), 
                         usudescripcion=sql.Literal(data['usudescripcion']), 
                         usuestado=sql.Literal(data['usuestado']), 
                         usuusureg=sql.Literal(data['usuusureg']))
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

# Gestionar Usuario Estado
def gestionarUsuarioEstado(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_usuario_gestionar_estado({tipo}, {usuid}, {usuusumod});
            ''').format( tipo=sql.Literal(data['tipo']), usuid=sql.Literal(data['usuid']), usuusumod=sql.Literal(data['usuusumod']))
        result = execute(as_string(query))
    except Exception as err:
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

# Gestionar Usuario Password(Contraseña)
def gestionarUsuarioPassword(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_usuario_password({usuid}, {usupassword}, {usuusumod});
            ''').format( usuid=sql.Literal(data['usuid']), usupassword = sql.Literal(generate_password_hash(data['usupassword'])), usuusumod=sql.Literal(data['usuusumod']))
        result = execute(as_string(query))
    except Exception as err:
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

# Lista de Usuarios
def listaUsuario():
    result = select(f'''
        SELECT 
        u.usuid, u.perid, p.pernomcompleto, p.pernrodoc, p.perfoto, u.rolid, r.rolnombre, u.usuname, 
        u.usuemail, u.usudescripcion, 
        u.usuestado, u.usuusureg, u.usufecreg, u.usuusumod, u.usufecmod
        FROM academico.usuario u
        inner join academico.persona p on p.perid = u.perid
        inner join academico.rol r on r.rolid = u.rolid 
        order by p.pernomcompleto 
    ''')    
    return result
    
def tipoPersona():
    return select(f''' 
    select perid, pernomcompleto, pernrodoc, perfoto from academico.persona p 
    where perestado = 1
    order by pernomcompleto;
    ''')

def perfil(data):
    return select(f'''
    SELECT u.usuid, u.perid, p.pernomcompleto, p.perfoto, u.rolid, r.rolnombre , u.usuname, u.usuemail 
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
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def obtenerEmail(data):
    res = select(f'''
    select usuid, usuname, usuemail from academico.usuario u where usuname = \'{data['usuname']}\' and usuemail = \'{data['usuemail']}\'
    ''')
    return res

