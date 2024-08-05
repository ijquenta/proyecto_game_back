import hashlib
from http import HTTPStatus
import os

import pytz
from models.matricula_model import Matricula
from models.tipo_matricula_model import TipoMatricula
from core.database import select, execute_function
from flask import jsonify, make_response
from dateutil import parser
from utils.date_formatting import *
from models.pago_model import Pago
from models.persona_model import Persona
from models.curso_materia_model import CursoMateria
from models.inscripcion_model import Inscripcion
from models.materia_model import Materia
from models.curso_model import Curso
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from core.database import db
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
def listarPago():
    return select('''
        SELECT pagid, pagdescripcion, pagmonto, pagarchivo, pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagfecha, pagtipo FROM academico.pago WHERE pagestado = 1;
    ''')

# parseGestionarPago.add_argument('tipo', type=int, help='Ingrese tipo', required=True)
# parseGestionarPago.add_argument('pagid', type=int, help='Ingrese pagid', required=True)
# parseGestionarPago.add_argument('insid', type=int, help='Ingrese insid', required=True)
# parseGestionarPago.add_argument('pagdescripcion', type=str, help='Ingrese pagdescripcion')
# parseGestionarPago.add_argument('pagmonto', type=int, help='Ingrese pagmonto', required=True)
# parseGestionarPago.add_argument('pagfecha', type=str, help='Ingrese pagfecha', required=True)
# parseGestionarPago.add_argument('pagusureg', type=str, help='Ingrese pagusureg', required=True)
# parseGestionarPago.add_argument('pagestadodescripcion', type=str, help='Ingrese pagestadodescripcion')
# parseGestionarPago.add_argument('pagestado', type=int, help='Ingrese pagestado')

def manage_pago(data, request):
    tipo = data.get('tipo')
    if tipo == 1:
        return create_pago(data, request)
    elif tipo == 2:
        return update_pago(data, request)
    elif tipo == 3:
        return delete_pago(data)
    else:
        return {"status": "error", "message": "Tipo de operación no soportada."}, HTTPStatus.BAD_REQUEST

from models.inscripcion_model import Inscripcion, db

"""
def create_pago(data):
    try:
        pago = Pago(
            pagdescripcion=data['pagdescripcion'],
            pagmonto=data['pagmonto'],
            pagusureg=data['pagusureg'],
            pagestado=data['pagestado'],
            pagfecha=data['pagfecha'],
            pagusumod=data['pagusureg'],
            pagfecreg=datetime.now(),
            pagfecmod=datetime.now(),
        )
        db.session.add(pago)
        db.session.commit()
        
        # Actualizar la inscripción
        inscripcion = Inscripcion.query.get(data['insid'])
        if inscripcion:
            inscripcion.pagid = pago.pagid
            db.session.commit()     
        
        return {"status": "success", "message": "Pago creado correctamente."}, HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Error al crear el pago: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
"""

def create_pago(data, request):
    try:
        # Configuración inicial
        archivos_permitidos = ['pagarchivo']
        archivos = {}
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'files_pago')
        os.makedirs(upload_directory, exist_ok=True)

        # Recuperar el documento existente si se proporciona un pagid
        pago_existente = Pago.query.filter_by(pagid=data.get('pagid')).first()

        if pago_existente:
            # Eliminar archivos existentes
            for archivo_key in archivos_permitidos:
                archivo_path = getattr(pago_existente, archivo_key, None)
                if archivo_path:
                    full_path = os.path.join(upload_directory, archivo_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)

        # Procesar archivos recibidos
        for archivo_key in archivos_permitidos:
            archivo = request.files.get(archivo_key)
            if archivo:
                if archivo.filename == '':
                    raise ValueError(f"Nombre de archivo vacío para {archivo_key}.")
                if allowed_file(archivo.filename):
                    # Calcular un nombre de archivo único utilizando un hash
                    file_hash = calculate_file_hash(archivo)
                    extension = archivo.filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{file_hash}.{extension}"
                    upload_path = os.path.join(upload_directory, unique_filename)

                    # Guardar el archivo si no existe
                    if not os.path.exists(upload_path):
                        archivo.save(upload_path)
                    archivos[archivo_key] = unique_filename
                else:
                    raise ValueError(f"Tipo de archivo no permitido para {archivo_key}.")
            else:
                archivos[archivo_key] = None  # No se proporciona archivo para esta clave

        
        # Crear un nuevo registro de pago
        nuevo_pago = Pago(
            pagdescripcion=data['pagdescripcion'],
            pagmonto=data['pagmonto'],              
            pagfecha=data['pagfecha'],
            pagusureg=data['pagusureg'],
            pagusumod=data['pagusureg'],
            pagtipo=data['pagtipo'],
            pagarchivo=archivos['pagarchivo'],
            pagestado=1,
            pagfecreg=datetime.now(),
            pagfecmod=datetime.now()
        )
        db.session.add(nuevo_pago)

        # Actualizar la inscripción con el nuevo ID de pago
        inscripcion = Inscripcion.query.get(data['insid'])
        if inscripcion:
            inscripcion.pagid = nuevo_pago.pagid

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El pago fue creado correctamente.",
            "filenames": {k: v for k, v in archivos.items() if v}
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al subir los archivos: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

def update_pago(data, request):
    try:
        # Configuración inicial
        archivos_permitidos = ['pagarchivo']
        archivos = {}
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'files_pago')
        os.makedirs(upload_directory, exist_ok=True)

        # Recuperar el registro de pago existente
        pago_existente = Pago.query.filter_by(pagid=data.get('pagid')).first()
        if not pago_existente:
            return make_response(jsonify({
                "status": "error",
                "message": "El pago especificado no existe."
            }), HTTPStatus.NOT_FOUND)

        # Eliminar archivos antiguos si se proporciona un archivo nuevo
        for archivo_key in archivos_permitidos:
            archivo_path = getattr(pago_existente, archivo_key, None)
            if archivo_path and request.files.get(archivo_key):
                full_path = os.path.join(upload_directory, archivo_path)
                if os.path.exists(full_path):
                    os.remove(full_path)

        # Procesar archivos recibidos
        for archivo_key in archivos_permitidos:
            archivo = request.files.get(archivo_key)
            if archivo:
                if archivo.filename == '':
                    raise ValueError(f"Nombre de archivo vacío para {archivo_key}.")
                if allowed_file(archivo.filename):
                    # Calcular un nombre de archivo único utilizando un hash
                    file_hash = calculate_file_hash(archivo)
                    extension = archivo.filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{file_hash}.{extension}"
                    upload_path = os.path.join(upload_directory, unique_filename)

                    # Guardar el archivo si no existe
                    if not os.path.exists(upload_path):
                        archivo.save(upload_path)
                    archivos[archivo_key] = unique_filename
                else:
                    raise ValueError(f"Tipo de archivo no permitido para {archivo_key}.")
            else:
                archivos[archivo_key] = getattr(pago_existente, archivo_key, None)  # Mantener el archivo existente si no se proporciona uno nuevo

        # Actualizar el registro de pago
        pago_existente.pagdescripcion = data.get('pagdescripcion', pago_existente.pagdescripcion)
        pago_existente.pagmonto = data.get('pagmonto', pago_existente.pagmonto)
        pago_existente.pagfecha = data.get('pagfecha', pago_existente.pagfecha)
        pago_existente.pagusumod = data.get('pagusumod', pago_existente.pagusumod)
        pago_existente.pagtipo = data.get('pagtipo', pago_existente.pagtipo)
        pago_existente.pagarchivo = archivos.get('pagarchivo', pago_existente.pagarchivo)
        pago_existente.pagfecmod = datetime.now()
        pago_existente.pagestado = data.get('pagestado', pago_existente.pagestado)

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El pago fue actualizado correctamente.",
            "filenames": {k: v for k, v in archivos.items() if v}
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al actualizar el pago: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)


"""
def update_pago(data):
    try:
        pago = Pago.query.get(data['pagid'])
        if pago:
            pago.pagdescripcion = data['pagdescripcion']
            pago.pagestadodescripcion = data['pagestadodescripcion']
            pago.pagmonto = data['pagmonto']
            pago.pagusumod = data['pagrusureg']
            pago.pagestado = data['pagestado']
            pago.pagfecha = datetime.strptime(data['pagfecha'], '%Y-%m-%d')  # Ajusta el formato de fecha según sea necesario
            db.session.commit()
            
            return {"status": "success", "message": "Pago modificada correctamente."}, HTTPStatus.OK
        else:
            return {"status": "error", "message": "Pago no encontrado."}, HTTPStatus.NOT_FOUND
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Error al actualizar el pago: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
"""

def delete_pago(data):
    try:
        pago = Pago.query.get(data['pagid'])
        if pago:
            db.session.delete(pago)
            db.session.commit()
            
            return {"status": "success", "message": "Pago eliminada correctamente."}, HTTPStatus.OK
        else:
            return {"status": "error", "message": "Pago no encontrado."}, HTTPStatus.NOT_FOUND
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Error al eliminar el pago: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

def gestionarPago(data):
    data = {key: f'\'{value}\'' if value is not None else 'NULL' for key, value in data.items()}

    return execute_function(f'''
       SELECT academico.f_gestionar_pago_2  
               ({data['tipo']},
                {data['pagid']}, 
                {data['insid']}, 
                {data['pagdescripcion']}, 
                {data['pagmonto']}, 
                {data['pagfecha']},
                {data['pagusureg']},
                {data['pagestadodescripcion']},                             
                {data['pagestado']}) as valor;
    ''')
    
def insertarPago(data):
    res = execute_function(f'''
       SELECT academico.f_pago_insertar (  
                \'{data['pagdescripcion']}\', 
                {data['pagmonto']}, 
                \'{data['pagfecha']}\',
                \'{data['pagarchivo']}\',
                \'{data['pagusureg']}\',
                {data['pagtipo']}
                ) as valor;
    ''')
    return res

def modificarPago(data):
    data['pagfecha'] = volverAFormatoOriginal(data['pagfecha']) 
    res = execute_function(f'''
       SELECT academico.f_pago_modificar (  
                  {data['pagid']}, 
                \'{data['pagdescripcion']}\', 
                  {data['pagmonto']}, 
                \'{data['pagarchivo']}\',
                \'{data['pagusumod']}\',
                \'{data['pagfecha']}\',
                  {data['pagtipo']},
                  {data['archivobol']}
                ) as valor;
    ''')
    return res

def asignarPagoInscripcion(data):
    res = execute_function(f'''
       SELECT academico.f_pago_asignar_a_inscripcion (  
                {data['insid']}, 
                {data['pagid']}, 
                \'{data['pagusumod']}\'
                ) as valor;
    ''')
    return res

def asignarPagoMatricula(data):
    res = execute_function(f'''
       SELECT academico.f_pago_asignar_a_matricula (  
                {data['matrid']}, 
                {data['pagid']}, 
                \'{data['matrusumod']}\'
                ) as valor;
    ''')
    return res


def obtenerUltimoPago():
    return select(f'''
       select pagid from academico.pago p where pagestado = 1 order by pagid desc limit 1
    ''') 
    
def listarPagoEstudiante(data):
    lista_pago_estudiante = select(f'''
         select distinct i.insid, i.matrid, cm.curid, 
               c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, i.peridestudiante, i.pagid, i.insusureg,
               i.insfecreg, i.insusumod, i.insfecmod, i.curmatid, i.insestado, i.insestadodescripcion 
            
          FROM academico.inscripcion i
          left join academico.curso_materia cm on cm.curmatid = i.curmatid
          left join academico.curso c on c.curid = cm.curid
          left join academico.materia m on m.matid = cm.matid
          LEFT JOIN academico.persona p ON p.perid = cm.periddocente
          where i.peridestudiante = {data['perid']}
          order by c.curnombre, m.matnombre; 
    ''')

    for pago_estudiante in lista_pago_estudiante:
        pago_estudiante["insfecreg"] = darFormatoFechaConHora(pago_estudiante["insfecreg"])
        pago_estudiante["insfecmod"] = darFormatoFechaConHora(pago_estudiante["insfecmod"])
        pago_estudiante["curmatfecini"] = darFormatoFechaSinHora(pago_estudiante["curmatfecini"])
        pago_estudiante["curmatfecfin"] = darFormatoFechaSinHora(pago_estudiante["curmatfecfin"])

    return lista_pago_estudiante


def getAllPaymentsForOneStudent(data):
    try:
        perid_estudiante = data.get('perid')

        # Definir alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    i.insid, i.matrid, cm.curid, c.curnombre, cm.curmatfecini,
                    cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente,
                    p.pernomcompleto, p.pernrodoc, i.peridestudiante, i.pagid, i.insusureg,
                    i.insfecreg, i.insusumod, i.insfecmod, i.curmatid,
                    i.insestado, i.insestadodescripcion
                )
                .outerjoin(cm, cm.curmatid == i.curmatid)
                .outerjoin(c, c.curid == cm.curid)
                .outerjoin(m, m.matid == cm.matid)
                .outerjoin(p, p.perid == cm.periddocente)
                .filter(i.peridestudiante == perid_estudiante)
                .order_by(c.curnombre, m.matnombre)
                .all())

        # Convertir los resultados en una lista de diccionarios
        lista_pago_estudiante = [
            {
                'insid': row.insid,
                'matrid': row.matrid,
                'curid': row.curid,
                'curnombre': row.curnombre,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'matid': row.matid,
                'matnombre': row.matnombre,
                'periddocente': row.periddocente,
                'pernomcompleto': row.pernomcompleto,
                'peridestudiante': row.peridestudiante,
                'pagid': row.pagid,
                'insusureg': row.insusureg,
                'insfecreg': row.insfecreg.isoformat() if row.insfecreg else None,
                'insusumod': row.insusumod,
                'insfecmod': row.insfecmod.isoformat() if row.insfecmod else None,
                'curmatid': row.curmatid,
                'insestado': row.insestado,
                'insestadodescripcion': row.insestadodescripcion
            } for row in query
        ]

        return make_response(jsonify(lista_pago_estudiante), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()

def listarPagoEstudianteMateria(data):
    return select(f'''
       SELECT distinct 
                i.insid, i.matrid, tm.tipmatrgestion, i.curmatid, c.curnombre, m2.matnombre, i.peridestudiante, p2.perfoto,
                i.pagid, p.pagdescripcion, p.pagmonto, p.pagarchivo, pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagtipo, pagfecha
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.pago p on p.pagid = i.pagid
        left join academico.persona p2 on p2.perid = i.peridestudiante
        where i.peridestudiante = {data['perid']}
        and cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
    ''') 


def getAllPaymentsCourse():
    try:
        # Definir alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        p = aliased(Persona)
        i = aliased(Inscripcion)
        pg = aliased(Pago)
        
        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
                    cm.curmatid,
                    cm.curid,
                    cm.curmatfecini,
                    cm.curmatfecfin,
                    cm.matid,
                    cm.curmatusureg,
                    cm.curmatfecreg,
                    cm.curmatusumod,
                    cm.curmatfecmod,
                    cm.curmatestadodescripcion,
                    cm.curmatdescripcion,
                    cm.periddocente,
                    cm.curmatestado,
                    c.curnombre,
                    m.matnombre,
                    p.pernomcompleto,
                    p.pernrodoc,
                    p.perfoto,
                    func.count(i.insid).label('num_estudiantes'),
                    func.count(pg.pagid).label('num_pagos'),
                    
                )
                .outerjoin(c, c.curid == cm.curid)
                .outerjoin(m, m.matid == cm.matid)
                .outerjoin(p, p.perid == cm.periddocente)
                .outerjoin(i, i.curmatid == cm.curmatid)
                .outerjoin(pg, pg.pagid == i.pagid)
                .group_by(cm.curmatid, c.curid, m.matid, p.perid)
                .order_by(c.curnombre, m.matnombre)
                .all())

        # Convertir los resultados en una lista de diccionarios
        listAllPaymentsCourse = [
            {
                'curmatid': row.curmatid,
                'curid': row.curid,
                'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None,
                'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None,
                'matid': row.matid,
                'curmatusureg': row.curmatusureg,
                'curmatfecreg': row.curmatfecreg.isoformat() if row.curmatfecreg else None,
                'curmatusumod': row.curmatusumod,
                'curmatfecmod': row.curmatfecmod.isoformat() if row.curmatfecmod else None,
                'curmatestadodescripcion': row.curmatestadodescripcion,
                'curmatdescripcion': row.curmatdescripcion,
                'curmatestado': row.curmatestado,       
                'periddocente': row.periddocente,
                'curnombre': row.curnombre,
                'matnombre': row.matnombre,
                'pernomcompleto': row.pernomcompleto,
                'pernrodoc': row.pernrodoc,
                'perfoto': row.perfoto,
                'num_estudiantes': row.num_estudiantes,
                'num_pagos': row.num_pagos,
            } for row in query
        ]

        return make_response(jsonify(listAllPaymentsCourse), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()
   

def listarPagoCurso():
    lista = select(f'''
        SELECT distinct cm.curmatid, cm.curid, c.curnombre, cm.curmatfecini, cm.curmatfecfin, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto p.pernrodoc, p.perfoto,
        cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, cm.curmatestadodescripcion, 
        cm.curmatdescripcion 
        FROM academico.curso_materia cm
        left join academico.curso c on c.curid = cm.curid 
        left join academico.materia m on m.matid = cm.matid 
        left join academico.persona p on p.perid = cm.periddocente 
        order by c.curnombre, m.matnombre;
    ''')  
    for pago in lista:
        pago["curmatfecreg"] = darFormatoFechaConHora(pago["curmatfecreg"])
        pago["curmatfecmod"] = darFormatoFechaConHora(pago["curmatfecmod"])
        pago["curmatfecini"] = darFormatoFechaSinHora(pago["curmatfecini"])
        pago["curmatfecfin"] = darFormatoFechaSinHora(pago["curmatfecfin"]) 
    return lista
    
def listarPagoEstudiantesMateria(data):
    lista = select(f'''
        SELECT distinct i.insid, i.curmatid, i.peridestudiante, 
                    i.pagid, m.matrid, tm.tipmatrgestion, cm.curid, c.curnombre, cm.matid, m2.matnombre, p2.pernomcompleto, p2.pernrodoc, 
                    p2.perfoto, p.pagfecha, p.pagdescripcion, p.pagmonto, p.pagarchivo, 
                    pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagtipo 
        FROM academico.inscripcion i 
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.tipo_matricula tm on m.tipmatrid = tm.tipmatrid
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.pago p on p.pagid = i.pagid 
        left join academico.persona p2 on p2.perid = i.peridestudiante 
        where cm.curid = {data['curid']}
        and cm.matid = {data['matid']}
    ''')
    for pago in lista:
        pago["pagfecreg"] = darFormatoFechaConHora(pago["pagfecreg"])
        pago["pagfecmod"] = darFormatoFechaConHora(pago["pagfecmod"])
        pago["pagfecha"] = darFormatoFechaConHora(pago["pagfecha"])
    return lista 

def getPagoEstudianteMateria(data):
    try:
        curid = data.get('curid')
        matid = data.get('matid')
        
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        p = aliased(Pago)
        p2 = aliased(Persona)
        tm = aliased(TipoMatricula)
        m = aliased(Matricula)
        m2 = aliased(Materia)
        i = aliased(Inscripcion)
        
        query = (db.session.query(
                    i.insid, i.curmatid, i.peridestudiante, i.pagid,
                    m.matrid, 
                    tm.tipmatrgestion, 
                    cm.curid, cm.matid,
                    c.curnombre, 
                    m2.matnombre, 
                    p2.pernomcompleto, p2.pernrodoc, p2.perfoto, 
                    p.pagfecha, p.pagdescripcion, p.pagmonto, p.pagarchivo, p.pagusureg, p.pagfecreg, p.pagusumod, p.pagfecmod, p.pagestado, p.pagtipo
                )
                .outerjoin(m, m.matrid == i.matrid)
                .outerjoin(cm, cm.curmatid == i.curmatid)
                .outerjoin(p, p.pagid == i.pagid)
                .outerjoin(p2, p2.perid == i.peridestudiante)
                .outerjoin(tm, tm.tipmatrid == m.tipmatrid)
                .outerjoin(m2, m2.matid == cm.matid)
                .outerjoin(c, c.curid == cm.curid)
                .filter(cm.curid == curid, cm.matid == matid)
                .all())
        
        lista_pago_estudiante_materia = [
            {
                'insid': row.insid,
                'curmatid': row.curmatid,
                'peridestudiante': row.peridestudiante,
                'pagid': row.pagid,
                'matrid': row.matrid,
                'tipmatrgestion': row.tipmatrgestion,
                'curid': row.curid,
                'matid': row.matid,
                'curnombre': row.curnombre,
                'matnombre': row.matnombre,
                'pernomcompleto': row.pernomcompleto,
                'pernrodoc': row.pernrodoc,
                'perfoto': row.perfoto,
                'pagfecha': row.pagfecha.isoformat() if row.pagfecha else None,
                'pagdescripcion': row.pagdescripcion,
                'pagmonto': row.pagmonto,
                'pagarchivo': row.pagarchivo,
                'pagusureg': row.pagusureg,
                'pagfecreg': row.pagfecreg.isoformat() if row.pagfecreg else None,
                'pagusumod': row.pagusumod,
                'pagfecmod': row.pagfecmod.isoformat() if row.pagfecmod else None,
                'pagestado': row.pagestado,
                'pagtipo': row.pagtipo
            } for row in query
        ]
        
        return make_response(jsonify(lista_pago_estudiante_materia), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {"error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    finally:
        db.session.close()
    
def tipoPago():
    return select(f'''
   select tp.tpagid, tp.tpagnombre from academico.tipo_pago tp              
    ''')    

def getPayments():
    pagos = Pago.query.all()
    pagos_json = [pago.to_dict() for pago in pagos]
    return make_response(jsonify(pagos_json), 200)

def getAllPayments():
    try:
        # Obtener los tipos de operación de la base de datos
        payments = Pago.query.order_by(Pago.pagid).all()
        # Convertir los datos en una lista de diccionarios
        response = [payment.to_dict() for payment in payments]
        # Retornar los datos como una respuesta JSON
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        # En caso de error, devolver un mensaje de error con el código de estado correspondiente
        error_response = {"error": "Error in the data base.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getPagoById(pagid):
    try:
        # Buscar el pago por ID
        pago = Pago.query.get(pagid)
        
        # Si no se encuentra el pago, devolver un error 404
        if pago is None:
            return make_response(jsonify({"error": "Pago no encontrado"}), HTTPStatus.NOT_FOUND)
        
        # Convertir el objeto `Pago` a un diccionario
        pago_data = pago.to_dict()
        
        # Crear la respuesta con el objeto `Pago`
        response_data = {
            "message": "Pago obtenido con éxito",
            "data": pago_data,
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
    
# Function to calculate the hash of a file
def calculate_file_hash(file):
    hasher = hashlib.md5()
    buf = file.read(1024)
    while buf:
        hasher.update(buf)
        buf = file.read(1024)
    file.seek(0)  # Reset file pointer to the beginning
    return hasher.hexdigest()

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS