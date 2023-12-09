from core.database import select, execute, execute_function, execute_response
from web.wsrrhh_service import *
from flask import Flask, request, jsonify, make_response

def listarNota():
    return select('''
        SELECT notid, insid, not1, not2, not3, notfinal, notusureg, notfecreg, notusumod, notfecmod, notestado FROM academico.nota;
    ''')

def registrarPersona(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT * FROM academico.registrar_persona
                ({pernombres}, {perapepat}, {perapemat}, 
                 {pertipodoc}, {pernrodoc},  {perusureg} 
                )
        ''').format(
            pernombres=sql.Literal(data['pernombres']),
            perapepat=sql.Literal(data['perapepat']),
            perapemat=sql.Literal(data['perapemat']),
            pertipodoc=sql.Literal(data['pertipodoc']),
            pernrodoc=sql.Literal(data['pernrodoc']),
            perusureg=sql.Literal(data['perusureg'])
        )
        result = execute_response(as_string(query)) 
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def gestionarPersona(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_gestionar_persona
                ({tipo},{perid}, {pernombres}, {perapepat}, {perapemat}, 
                 {pertipodoc}, {pernrodoc}, {perfecnac}, {perdirec}, {peremail}, 
                 {percelular}, {pertelefono}, {perpais}, {perciudad}, {pergenero}, 
                 {perestcivil}, {perfoto}, {perestado}, {perobservacion}, {perusureg}, 
                 {perusumod})
        ''').format(
            tipo=sql.Literal(data['tipo']),
            perid=sql.Literal(data['perid']),
            pernombres=sql.Literal(data['pernombres']),
            perapepat=sql.Literal(data['perapepat']),
            perapemat=sql.Literal(data['perapemat']),
            pertipodoc=sql.Literal(data['pertipodoc']),
            pernrodoc=sql.Literal(data['pernrodoc']),
            perfecnac=sql.Literal(data['perfecnac']),
            perdirec=sql.Literal(data['perdirec']),
            peremail=sql.Literal(data['peremail']),
            percelular=sql.Literal(data['percelular']),
            pertelefono=sql.Literal(data['pertelefono']),
            perpais=sql.Literal(data['perpais']),
            perciudad=sql.Literal(data['perciudad']),
            pergenero=sql.Literal(data['pergenero']),
            perestcivil=sql.Literal(data['perestcivil']),
            perfoto=sql.Literal(data['perfoto']),
            perestado=sql.Literal(data['perestado']),
            perobservacion=sql.Literal(data['perobservacion']),
            perusureg=sql.Literal(data['perusureg']),
            perusumod=sql.Literal(data['perusumod']),
        )
        result = execute(as_string(query)) 
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def tipoDocumento():
    return select('''
        SELECT tipodocid, tipodocnombre
        FROM academico.tipo_documento;
    ''')
def tipoEstadoCivil():
    return select('''
        SELECT estadocivilid, estadocivilnombre
        FROM academico.tipo_estadocivil;
    ''')
def tipoGenero():
    return select('''
        SELECT generoid, generonombre
        FROM academico.tipo_genero;
    ''')
def tipoPais():
    return select('''
        SELECT paisid, paisnombre
        FROM academico.tipo_pais;
    ''')
def tipoCiudad():
    return select('''
        SELECT ciudadid, ciudadnombre, paisid
        FROM academico.tipo_ciudad;
    ''')
    
def listarUsuarios():
    return select(f'''
    SELECT id, nombre_usuario, contrasena, nombre_completo, rol
    FROM public.usuarios;
    ''')

