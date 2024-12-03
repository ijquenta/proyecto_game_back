from http import HTTPStatus
from models.materia_model import Materia
from core.database import select, as_string, execute, execute_function
from psycopg2 import sql
from flask import jsonify, make_response
from utils.date_formatting import *


def listarMateria():
    lista_materias = select(f'''
    SELECT matid, matnombre, matdescripcion, matusureg, matfecreg, matusumod, matfecmod, matestado, matestadodescripcion, matnivel, matdesnivel
    FROM academico.materia
    order by matid desc;        
    ''')
    return lista_materias


def listaMateriaCombo(data):
    return select(f'''
        select distinct m.matid, m.matnombre, m.matnivel 
        FROM academico.materia m
        inner join academico.curso c on c.curnivel = m.matnivel
        where m.matnivel = {data['curnivel']}         
        ''')


def getListMateriaCombo():
    return select(f'''
        select distinct m.matid, m.matnombre
        FROM academico.materia m
        where m.matestado = 1
        order by m.matnombre         
        ''')


def eliminarMateria(data):
    resultado = execute_function(f'''
    SELECT academico.eliminar_materia({data['matid']}) as valor;
    ''')
    result = resultado[0]['valor']
    if result == 1:
        response_data = {'message': 'Materia eliminado correctamente'}
        status_code = 200
    else:
        if result == 0:
            response_data = {'message': 'No se pudo eliminar el materia'}
            status_code = 500
        else:
            response_data = {
                'message': 'No se puede eliminar la materia debido a que tiene registros relacionados'}
            status_code = 500
        print("response_data: ", response_data)

    return make_response(jsonify(response_data), status_code)


def insertarMateria(data):
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


def gestionarMateriaEstado(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_materia_gestionar_estado({tipo}, {matid}, {matusumod});
            ''').format(
            tipo=sql.Literal(data['tipo']),
            matid=sql.Literal(data['matid']),
            matusumod=sql.Literal(data['matusumod'])
        )
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result


def getMateriaById(matid):
    try:
        # Buscar el materia por ID
        materia = Materia.query.get(matid)

        # Si no se encuentra el materia, devolver un error 404
        if materia is None:
            return make_response(jsonify({"error": "Materia no encontrado"}), HTTPStatus.NOT_FOUND)

        # Convertir el objeto `Materia` a un diccionario
        materia_data = materia.to_dict()

        # Crear la respuesta con el objeto `Materia`
        response_data = {
            "message": "Materia obtenido con éxito",
            "data": materia_data,
            "code": HTTPStatus.OK
        }

        return make_response(jsonify(response_data), HTTPStatus.OK)

    except Exception as e:
        # Manejar cualquier error inesperado
        error_response = {
            "error": "Error en la base de datos",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
