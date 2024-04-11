from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from datetime import datetime

def darFormatoFecha(fecha_str):
    if fecha_str is None:
       return None
    # Convertir la cadena de fecha a un objeto datetime
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Formatear la fecha como desees, por ejemplo, "DD/MM/AAAA HH:MM:SS"
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y %H:%M:%S")

    return fecha_formateada

def listarMateria():
    lista_materias = select(f'''
    SELECT matid, matnombre, matdescripcion, matusureg, matfecreg, matusumod, matfecmod, matestado, matestadodescripcion, matnivel, matdesnivel
    FROM academico.materia
    order by matid desc;        
    ''')
    
    for materia in lista_materias:
        materia["matfecreg"] = darFormatoFecha(materia["matfecreg"])
        materia["matfecmod"] = darFormatoFecha(materia["matfecmod"])
    
    return lista_materias
    
    
def listaMateriaCombo(data):
    return select(f'''
        select distinct m.matid, m.matnombre, m.matnivel 
        FROM academico.materia m
        inner join academico.curso c on c.curnivel = m.matnivel
        where m.matnivel = {data['curnivel']}         
        ''')

def crearRol(data):
    # print("Datos->",data)
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
    # print("Datos->",data)
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
        query = sql.SQL('''
            select * from f_rol_eliminar({rolId});
            ''').format(
                rolId=sql.Literal(data['rolId'])  
            )
        # print("Consulta SQL:", query, data['rolId'])  
        result = execute(as_string(query))
        print(result)
    except Exception as err:
        print("Error:", err)  
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def listarPersona():
    return select(f'''
    SELECT
    p.perid, p.perusuario, p.percontrasena, p.percontrasenaconfirmar,
    p.pernombres, p.perapepat, p.perapemat, p.perfecnac, p.perdomicilio,
    p.peridpais, p.perpais, p.peridgenero, p.pergenero, p.percorreoelectronico,
    p.percelular, p.pertelefono, p.perfoto, p.perusureg, p.perfecreg,
    p.perusumod, p.perfecmod, p.perestado,r.rolid, r.rolnombre, p.pernombrecompleto
    FROM academico.persona p
    LEFT JOIN academico.roles r ON p.peridrol = r.rolid
    WHERE p.perestado = 1;
    ''')


def eliminarMateria(data):
    resultado = execute_function(f'''
    SELECT academico.eliminar_materia({data['matid']}) as valor;
    ''')
    result = resultado[0]['valor']
    # print("Resultado: ", result)
    if result == 1:
        response_data = {'message': 'Materia eliminado correctamente'}
        status_code = 200
    else:
        if result == 0:
            response_data = {'message': 'No se pudo eliminar el materia'}
            status_code = 500
        else:
            response_data = {'message': 'No se puede eliminar la materia debido a que tiene registros relacionados'}
            status_code = 500
        # print("response_data: ",response_data)    

    return make_response(jsonify(response_data), status_code)

def insertarMateria(data):
    # print("Insertar Materia ->", data)
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.insertar_materia({matnombre}, {matdescripcion}, {matnivel}, {matdesnivel}, {matestado}, {matestadodescripcion}, {matusureg});
            ''').format(
                matnombre=sql.Literal(data['matnombre']),
                matdescripcion=sql.Literal(data['matdescripcion']),
                matnivel=sql.Literal(data['matnivel']),
                matdesnivel=sql.Literal(data['matdesnivel']),
                matestado=sql.Literal(data['matestado']),
                matestadodescripcion=sql.Literal(data['matestadodescripcion']),
                matusureg=sql.Literal(data['matusureg'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def modificarMateria(data):
    # print("Modificar Materia ->", data)
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.modificar_materia({matid}, {matnombre}, {matdescripcion}, {matnivel}, {matdesnivel}, {matestado}, {matestadodescripcion}, {matusumod});
            ''').format(
                matid=sql.Literal(data['matid']),
                matnombre=sql.Literal(data['matnombre']),
                matdescripcion=sql.Literal(data['matdescripcion']),
                matnivel=sql.Literal(data['matnivel']),
                matdesnivel=sql.Literal(data['matdesnivel']),
                matestado=sql.Literal(data['matestado']),
                matestadodescripcion=sql.Literal(data['matestadodescripcion']),
                matusumod=sql.Literal(data['matusumod'])
            )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result
