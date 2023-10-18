from core.database import select, execute, execute_function
from core.database import execute, as_string
from psycopg2 import sql



def listarRoles():
    return select(f'''
    SELECT rolid, rolnombre, roldescripcion, rolusureg, rolfecreg, rolusumod, rolfecmod, rolestado
    FROM academico.roles
    where rolestado = 1
    order by rolid;        
    ''')

def crearRol(data):
    print("Datos->",data)
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT * from academico.agregarrol({rolNombre}, {rolDescripcion}, {rolUsuReg});
            ''').format(
                rolNombre=sql.Literal(data['rolNombre']),
                rolDescripcion=sql.Literal(data['rolDescripcion']),
                rolUsuReg=sql.Literal(data['rolUsuReg'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def modificarRol(data):
    print("Datos->",data)
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.modificarrol2({rolId}, {rolNombre}, {rolDescripcion}, {rolUsuMod});
            ''').format(
                rolId=sql.Literal(data['rolId']),
                rolNombre=sql.Literal(data['rolNombre']),
                rolDescripcion=sql.Literal(data['rolDescripcion']),
                rolUsuMod=sql.Literal(data['rolUsuMod'])
            )
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
            ''').format(
                rolid=sql.Literal(data['rolid']),
                rolusumod=sql.Literal(data['rolusumod'])
            )
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
        # Verifica la consulta SQL generada imprimiéndola antes de ejecutarla.
        query = sql.SQL('''
            select * from f_rol_eliminar({rolId});
            ''').format(
                rolId=sql.Literal(data['rolId'])  # Usar data.get() para manejar posibles valores nulos.
            )
        print("Consulta SQL:", query, data['rolId'])  # Agrega esta línea para depurar la consulta SQL.
        # Asegúrate de que 'execute' esté definida y funcione correctamente.
        result = execute(as_string(query))
        print(result)
    except Exception as err:
        print("Error:", err)  # Imprime el error original para facilitar la depuración.
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def listarPersona():
    return select(f'''
    SELECT
    p.perid, p.perusuario, p.percontrasena, p.percontrasenaconfirmar,
    p.pernombres, p.perapepat, p.perapemat, p.perfecnac, p.perdomicilio,
    p.peridpais, p.perpais, p.peridgenero, p.pergenero, p.percorreoelectronico,
    p.percelular, p.pertelefono, p.perfoto, p.perusureg, p.perfecreg,
    p.perusumod, p.perfecmod, p.perestado,r.rolid, r.rolnombre
    FROM academico.persona p
    LEFT JOIN academico.roles r ON p.peridrol = r.rolid
    WHERE p.perestado = 1;
    ''')
