from core.database import select, execute, execute_function
from core.database import execute, as_string
from psycopg2 import sql
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

def gestionarRol(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_gestionar_rol({tipo}, {rolid}, {rolnombre}, {roldescripcion}, {rolestado}, {rolusureg});
            ''').format(
                tipo=sql.Literal(data['tipo']),
                rolid=sql.Literal(data['rolid']),
                rolnombre=sql.Literal(data['rolnombre']),
                roldescripcion=sql.Literal(data['roldescripcion']),
                rolestado=sql.Literal(data['rolestado']),
                rolusureg=sql.Literal(data['rolusureg'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print("Error en Gestionar Rol: ",err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def gestionarRolEstado(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_rol_gestionar_estado({tipo}, {rolid}, {rolusumod});
            ''').format(
                tipo=sql.Literal(data['tipo']),
                rolid=sql.Literal(data['rolid']),
                rolusumod=sql.Literal(data['rolusumod'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print("Error en Gestionar Rol Estado: ", err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

def listarRoles():
    listRoles = select(f'''
    SELECT rolid, rolnombre, roldescripcion, rolusureg, rolfecreg, rolusumod, rolfecmod, rolestado
    FROM academico.rol
    order by rolid;        
    ''')

    for rol in listRoles:
        rol["rolfecreg"] = darFormatoFecha(rol["rolfecreg"])
        rol["rolfecmod"] = darFormatoFecha(rol["rolfecmod"])
    
    return listRoles
    
def crearRol(data):
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
        query = sql.SQL('''
            select * from f_rol_eliminar({rolId});
            ''').format(
                rolId=sql.Literal(data['rolId'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print("Error:", err)  
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def listarPersona():
    return select(f'''
    SELECT perid, pernomcompleto, pernombres, perapepat, perapemat, pertipodoc, pernrodoc, perfecnac, perdirec, peremail, percelular, pertelefono, perpais, perciudad, pergenero, perestcivil, perfoto, perestado, perobservacion, perusureg, perfecreg, perusumod, perfecmod 
    FROM academico.persona
    ORDER BY perid desc;
    ''')