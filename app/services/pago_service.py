# Importaciones estándar de Python
import os
import hashlib
import decimal
from datetime import datetime
from http import HTTPStatus

# Importaciones de Flask
from flask import jsonify, make_response

# Importaciones de SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy import case

# Importaciones del core del proyecto
from core.database import select, execute_function, db
from core.rml.report_generator import Report

# Importaciones de modelos
from models.matricula_model import Matricula
from models.inscripcion_model import Inscripcion
from models.tipo_matricula_model import TipoMatricula
from models.pago_model import Pago, TipoPago
from models.nota_model import Nota
from models.persona_model import Persona
from models.curso_materia_model import CursoMateria
from models.materia_model import Materia
from models.curso_model import Curso

# Importaciones de utilidades
from utils.date_formatting import *


def make(pdf):
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(
        "archivo.pdf")
    response.mimetype = 'application/pdf'
    return response


def listarPago():
    return select('''
        SELECT pagid, pagdescripcion, pagmonto, pagarchivo, pagusureg, pagfecreg, pagusumod, pagfecmod, pagestado, pagfecha, pagtipo FROM academico.pago WHERE pagestado = 1;
    '''
                  )

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
    
def getAllPaymentsForOneStudent(data):
    try:
        # Definir alias para las tablas
        i = aliased(Inscripcion)
        mt = aliased(Matricula)
        tm = aliased(TipoMatricula)
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)
        pa = aliased(Pago)
        p = aliased(Persona)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
            i.insid, i.matrid, tm.tipmatrgestion, i.curmatid,
            c.curid, c.curnombre, m.matid, m.matnombre, i.peridestudiante, p.perfoto,
            i.pagid, c.curfchini, c.curfchfin, cm.curmatestado,
            pa.pagdescripcion, pa.pagmonto, pa.pagarchivo, pa.pagusureg, pa.pagfecreg,
            pa.pagusumod, pa.pagfecmod, pa.pagestado, pa.pagtipo, pa.pagfecha,
        )
            .join(mt, mt.matrid == i.matrid)
            .join(tm, tm.tipmatrid == mt.tipmatrid)
            .join(cm, cm.curmatid == i.curmatid)
            .join(c, c.curid == cm.curid)
            .join(m, m.matid == cm.matid)
            .join(pa, pa.pagid == i.pagid)
            .join(p, p.perid == i.peridestudiante)
            .distinct()
            .filter(i.peridestudiante == data['perid'])
            .all())
        
        lista_pago_estudiante = [
            {
                'insid': row.insid,
                'pagid': row.pagid,
                'pagdescripcion': row.pagdescripcion,
                'pagmonto': row.pagmonto,
                'pagarchivo': row.pagarchivo,
                'pagusureg': row.pagusureg,
                'pagfecreg': row.pagfecreg.isoformat() if row.pagfecreg else None,
                'pagusumod': row.pagusumod,
                'pagfecmod': row.pagfecmod.isoformat() if row.pagfecmod else None,
                'pagestado': row.pagestado,
                'pagtipo': row.pagtipo,
                'pagfecha': row.pagfecha.isoformat() if row.pagfecha else None,
                'curmatid': row.curmatid,
                'curid': row.curid,
                'curnombre': row.curnombre,
                'curfchini': row.curfchini.isoformat() if row.curfchini else None,
                'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,  
                'curmatestado': row.curmatestado,
                'matid': row.matid,
                'matnombre': row.matnombre,
                'matrid': row.matrid,
                'tipmatrgestion': row.tipmatrgestion,
                'peridestudiante': row.peridestudiante,
                'perfoto': row.perfoto,
            } for row in query]

        return make_response(jsonify(lista_pago_estudiante), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.session.close()

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
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
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
        error_response = {
            "error": "Error en la base de datos.", "message": str(e)}
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
        error_response = {
            "error": "Error in the data base.", "message": str(e)}
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

def calculateFileHash(file):
    hasher = hashlib.md5()
    buf = file.read(1024)
    while buf:
        hasher.update(buf)
        buf = file.read(1024)
    file.seek(0)  # Reset file pointer to the beginning
    return hasher.hexdigest()

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
    -----------------------------------------------------------------------------------------------------------
    Payment's Fuctions
    Admistrar pago 
    - por tipo: para crear, modificar y eliminar
    - Adminstrar pagos asignados a matriculas
"""

def allowedFile(filename):
    # Extensiones permitidas
    allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def calculateFileHash(file):
    # Calcula un hash SHA256 para el archivo
    hasher = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hasher.update(chunk)
    file.seek(0)  # Resetea el cursor del archivo después de leerlo
    return hasher.hexdigest()

def saveFilePago(request):
    # Configuración inicial
    archivo_key = 'pagarchivo'
    basepath = os.path.dirname(__file__)
    upload_directory = os.path.join(basepath, '..', 'static', 'files_pago')
    os.makedirs(upload_directory, exist_ok=True)

    archivo = request.files.get(archivo_key)
    if archivo:
        if archivo.filename == '':
            raise ValueError(f"Nombre de archivo vacío para {archivo_key}.")
        if allowedFile(archivo.filename):
            file_hash = calculateFileHash(archivo)
            extension = archivo.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{file_hash}.{extension}"
            upload_path = os.path.join(upload_directory, unique_filename)

            # Guardar el archivo solo si no existe
            if not os.path.exists(upload_path):
                archivo.save(upload_path)
            return unique_filename
        else:
            raise ValueError(
                f"Tipo de archivo no permitido para {archivo_key}.")
    return None

""" Administrar pago por tipo
"""
def managePayment(data, request):
    tipo = data.get('tipo')
    if tipo == 1:
        return createPayment(data, request)
    elif tipo == 2:
        return updatePayment(data, request)
    elif tipo == 3:
        return deletePayment(data)
    else:
        return {"status": "error", "message": "Tipo de operación no soportada."}, HTTPStatus.BAD_REQUEST

# Crear pago además de guardar el archivo si se proporciona
def createPayment(data, request):
    try:
        # Verificar si la inscripción ya tiene un pago asignado
        inscripcion = Inscripcion.query.get(data['insid'])
        if not inscripcion:
            resp = {
                "status": "error",
                "message": f"No se encontró la inscripción con ID {data['insid']}."
            }
            return make_response(jsonify(resp), HTTPStatus.NOT_FOUND)

        if inscripcion.pagid:
            resp = {
                "status": "error",
                "message": "Esta inscripción ya tiene un pago asignado.",
                "existing_payment_id": inscripcion.pagid
            }
            return make_response(jsonify(resp), HTTPStatus.CONFLICT)

        # Guardar el archivo de request
        archivo = saveFilePago(request)

        # Crear un nuevo registro de pago
        nuevo_pago = Pago(
            pagdescripcion=data['pagdescripcion'],
            pagmonto=data['pagmonto'],
            pagfecha=data['pagfecha'],
            pagusureg=data['pagusureg'],
            pagusumod=data['pagusureg'],
            pagtipo=data['pagtipo'],
            pagarchivo=archivo,  # Guardar el nombre del archivo guardado
            pagestado=1,  # Estado del pago (1 = activo)
            pagfecreg=datetime.now(),
            pagfecmod=datetime.now()
        )
        db.session.add(nuevo_pago)
        db.session.flush()  # Asegura que el nuevo pago obtenga un pagid antes de commit

        # Asignar el nuevo pago a la inscripción
        inscripcion.pagid = nuevo_pago.pagid
        inscripcion.matrusumod = datetime.now()  # Actualiza la fecha de modificación

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El pago fue creado y asignado a la inscripción correctamente.",
            "pago": nuevo_pago.to_dict()  # Devuelve los detalles del nuevo pago
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al crear y asignar el pago: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.pago_model import Pago, db
def updatePayment(data, request):
    try:
        # Guardar el archivo de request utilizando la función saveFilePago
        archivo = saveFilePago(request)

        # Recuperar el registro de pago existente
        pago_existente = Pago.query.filter_by(pagid=data.get('pagid')).first()
        if not pago_existente:
            return make_response(jsonify({
                "status": "error",
                "message": "El pago especificado no existe."
            }), HTTPStatus.NOT_FOUND)

        # Eliminar el archivo antiguo si se proporciona un archivo nuevo
        if archivo:
            # Si hay un archivo nuevo y existe uno antiguo, eliminar el antiguo
            if pago_existente.pagarchivo:
                basepath = os.path.dirname(__file__)
                old_file_path = os.path.join(
                    basepath, '..', 'static', 'files_pago', pago_existente.pagarchivo)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            # Asignar el nuevo archivo al registro de pago
            pago_existente.pagarchivo = archivo

        # Actualizar el resto de los campos del registro de pago
        pago_existente.pagdescripcion = data.get(
            'pagdescripcion', pago_existente.pagdescripcion)
        pago_existente.pagmonto = data.get('pagmonto', pago_existente.pagmonto)
        pago_existente.pagfecha = data.get('pagfecha', pago_existente.pagfecha)
        pago_existente.pagusumod = data.get(
            'pagusumod', pago_existente.pagusumod)
        pago_existente.pagtipo = data.get('pagtipo', pago_existente.pagtipo)
        pago_existente.pagfecmod = datetime.now()
        pago_existente.pagestado = data.get(
            'pagestado', pago_existente.pagestado)

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El pago fue actualizado correctamente.",
            "pago": pago_existente.to_dict()
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al actualizar el pago: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

def deletePayment(data):
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

def manageAssignPayment(data, request):
    tipo = data.get('tipo')
    if tipo == 1:
        return createAndAssignPayment(data, request)
    elif tipo == 2:
        return modifyPaymentAlreadyAssigned(data, request)
    else:
        return {"status": "error", "message": "Tipo de operación no soportada."}, HTTPStatus.BAD_REQUEST

def createAndAssignPayment(data, request):
    try:
        # Verificar si la matrícula existe
        matricula = Matricula.query.get(data['matrid'])
        if not matricula:
            resp = {
                "status": "error",
                "message": f"No se encontró la matrícula con ID {data['matrid']}."
            }
            return make_response(jsonify(resp), HTTPStatus.NOT_FOUND)

        # Verificar si la matrícula ya tiene un pago asignado
        if matricula.pagoidmatricula:
            resp = {
                "status": "error",
                "message": "Esta matrícula ya tiene un pago asignado.",
                "existing_payment_id": matricula.pagoidmatricula
            }
            return make_response(jsonify(resp), HTTPStatus.CONFLICT)

        # Guardar el archivo
        archivo = saveFilePago(request)

        # Crear un nuevo registro de pago
        nuevo_pago = Pago(
            pagdescripcion=data['pagdescripcion'],
            pagmonto=data['pagmonto'],
            pagfecha=data['pagfecha'],
            pagusureg=data['pagusureg'],
            pagusumod=data['pagusureg'],
            pagtipo=data['pagtipo'],
            pagarchivo=archivo,
            # Estado por defecto = 1 si no se proporciona
            pagestado=data.get('pagestado', 1),
            pagfecreg=datetime.now(),
            pagfecmod=datetime.now()
        )
        db.session.add(nuevo_pago)
        db.session.flush()  # Asegura que el nuevo pago obtenga un pagid

        # Asignar el pago a la matrícula
        matricula.pagoidmatricula = nuevo_pago.pagid
        matricula.matrusumod = datetime.now()

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El pago fue creado y asignado a la matrícula correctamente.",
            "pago": nuevo_pago.to_dict(),
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al crear y asignar el pago: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

def modifyPaymentAlreadyAssigned(data, request):
    try:
        # Guardar el archivo nuevo (si se proporciona uno)
        archivo = saveFilePago(request)

        # Obtener el registro de pago existente
        pago = Pago.query.get(data['pagid'])
        if not pago:
            raise ValueError(f"No se encontró el pago con ID {data['pagid']}.")

        # Eliminar el archivo anterior si se ha subido uno nuevo
        if archivo and pago.pagarchivo:
            old_file_path = os.path.join(os.path.dirname(
                __file__), '..', 'static', 'files_pago', pago.pagarchivo)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        # Actualizar los campos del pago
        pago.pagdescripcion = data.get('pagdescripcion', pago.pagdescripcion)
        pago.pagmonto = data.get('pagmonto', pago.pagmonto)
        pago.pagfecha = data.get('pagfecha', pago.pagfecha)
        pago.pagusumod = data['pagusumod']
        pago.pagtipo = data.get('pagtipo', pago.pagtipo)
        if archivo:
            pago.pagarchivo = archivo
        pago.pagfecmod = datetime.now()

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El pago fue modificado correctamente.",
            "pago": pago.to_dict(),
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al modificar el pago: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

def rptPagoEstudianteMateria(data):
    try:
        # Definir los alias para las tablas
        cm = aliased(CursoMateria)
        c = aliased(Curso)
        m = aliased(Materia)    
        i = aliased(Inscripcion)
        pe = aliased(Persona)
        tm = aliased(TipoMatricula)
        pa = aliased(Pago)
        mt = aliased(Matricula)
        tp = aliased(TipoPago)

        query = (db.session.query(
                    i.insid, i.matrid, tm.tipmatrgestion, i.curmatid,
                    c.curid, c.curnombre, m.matid, m.matnombre, i.peridestudiante, pe.pernomcompleto, pe.perfoto, pe.pernrodoc, pe.peremail, pe.percelular,
                    i.pagid, c.curfchini, c.curfchfin, cm.curmatestado,
                    pa.pagdescripcion, cm.curmatcosto,
                    pa.pagmonto, pa.pagusureg, pa.pagfecreg,
                    case([(pa.pagarchivo != None, 'Sí')], else_='No').label('pagarchivo'),
                    case(
                        [
                            (pa.pagestado == 1, 'Pagado'),        # Si pagestado es 1, es "Pagado"
                            (pa.pagestado == 2, 'Pendiente'),     # Si pagestado es 2, es "Pendiente"
                            (pa.pagestado == 0, 'Sin pagar'),     # Si pagestado es 0, es "Sin pagar"
                            (pa.pagestado == None, 'Sin pagar')   # Si pagestado es None, es "Sin pagar"
                        ],
                        else_='Ninguno'  # Si es cualquier otro número, es "Ninguno"
                    ).label('pagestado'),
                    pa.pagusumod, pa.pagfecmod, pa.pagtipo, pa.pagfecha,
                    cm.curmatfecini, cm.curmatfecfin, tp.tpagnombre  
                )
                    .join(mt, mt.matrid == i.matrid)
                    .join(tm, tm.tipmatrid == mt.tipmatrid)
                    .join(cm, cm.curmatid == i.curmatid)
                    .join(c, c.curid == cm.curid)
                    .join(m, m.matid == cm.matid)
                    .join(pa, pa.pagid == i.pagid)
                    .join(tp, pa.pagtipo == tp.tpagid)
                    .join(pe, pe.perid == i.peridestudiante)
                    .filter(i.peridestudiante == data['perid'])
                    .distinct()
                    .all())
        
        # Inicializar un diccionario para agrupar los cursos
        cursos_agrupados = {}

        # Inicializar el diccionario para la información del estudiante
        estudiante = {}

        # Iterar sobre los resultados de la consulta y agrupar por curnombre
        for row in query:
            # Generar la llave basada en curnombre y las fechas del curso-materia
            llave = row.curnombre + ' ' + row.curfchini.isoformat() + ' - ' + row.curfchfin.isoformat()

            # Crear el objeto de la lista
            elemento = {
                'curso_materia': { 
                        'curmatfecini': row.curmatfecini.isoformat() if row.curmatfecini else None, 
                        'curmatfecfin': row.curmatfecfin.isoformat() if row.curmatfecfin else None, 
                        'matid': row.matid, 
                        'matnombre': row.matnombre, 
                        'curid': row.curid, 
                        'curnombre': row.curnombre, 
                        'curfchini': row.curfchini.isoformat() if row.curfchini else None, 
                        'curfchfin': row.curfchfin.isoformat() if row.curfchfin else None,
                        'curmatcosto': row.curmatcosto 
                    },
                'pago': {
                        'pagid': row.pagid,
                        'pagdescripcion': row.pagdescripcion,
                        'pagmonto': row.pagmonto,
                        'pagarchivo': row.pagarchivo,
                        'pagusureg': row.pagusureg,
                        'pagfecreg': row.pagfecreg.isoformat() if row.pagfecreg else None,
                        'pagusumod': row.pagusumod,
                        'pagfecmod': row.pagfecmod.isoformat() if row.pagfecmod else None,
                        'pagestado': row.pagestado,
                        'pagtipo': row.pagtipo,
                        'pagfecha': row.pagfecha.isoformat() if row.pagfecha else None,
                        'tpagnombre': row.tpagnombre
                    }
            }

            # Asignar la información del estudiante (solo una vez)
            if not estudiante:
                estudiante = { 
                    'pernomcompleto': row.pernomcompleto,
                    'pernrodoc': row.pernrodoc,
                    'peremail': row.peremail,
                    'percelular': row.percelular,
                    'perfoto': row.perfoto
                }

            # Si la llave ya existe en el diccionario, agregamos el elemento a la lista
            if llave in cursos_agrupados:
                cursos_agrupados[llave].append(elemento)
            else:
                # Si la llave no existe, la creamos con una lista que contiene el elemento
                cursos_agrupados[llave] = [elemento]

      
        # Generar y devolver el reporte en PDF
        return make(Report().RptPagoEstudianteMateria(cursos_agrupados, estudiante, data['usuname']))

    except Exception as e:
        db.session.rollback()
        print(f"Error rpt PagoEstudianteMateria: {e}")
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def generarComprobantePagoEstudiante(data):
    try:
        # Definir los alias para las tablas
        i = aliased(Inscripcion)
        p = aliased(Persona)
        pa = aliased(Pago)
        c = aliased(Curso)
        cm = aliased(CursoMateria)
        m = aliased(Materia)
        tp = aliased(TipoPago)

        # Realizar la consulta para obtener el pago y la información relevante
        query = (db.session.query(
                    i.insid, i.peridestudiante, i.curmatid, c.curfchini, c.curfchfin, cm.curmatcosto,
                    p.pernomcompleto, p.pernrodoc, p.peremail, p.percelular, p.perfoto, pa.pagarchivo, pa.pagfecha, pa.pagid,
                    pa.pagid, pa.pagmonto, pa.pagdescripcion, pa.pagfecreg, pa.pagestado, pa.pagusumod, pa.pagfecmod,
                    c.curnombre, cm.curmatfecini, cm.curmatfecfin, m.matnombre, tp.tpagnombre
                )
                .join(p, p.perid == i.peridestudiante)
                .join(pa, pa.pagid == i.pagid)
                .join(cm, cm.curmatid == i.curmatid)
                .join(c, c.curid == cm.curid)
                .join(m, m.matid == cm.matid)
                .join(tp, tp.tpagid == pa.pagtipo)
                .filter(i.insid == data['insid'])
                .filter(i.peridestudiante == data['perid'])
                .first())

        if not query:
            return make_response(jsonify({'error': 'No se encontraron registros para el estudiante.'}), HTTPStatus.NOT_FOUND)

        # Organizar los datos del comprobante
        comprobante = {
            'estudiante': {
                'pernomcompleto': query.pernomcompleto,
                'pernrodoc': query.pernrodoc,
                'peremail': query.peremail,
                'percelular': query.percelular,
                'perfoto': query.perfoto
            },
            'curso': {
                'curnombre': query.curnombre,
                'matnombre': query.matnombre,
                'curmatcosto': query.curmatcosto,
                'curfchini': query.curfchini.isoformat() if query.curfchini else None,
                'curfchfin': query.curfchfin.isoformat() if query.curfchfin else None,
                'curmatfecini': query.curmatfecini.isoformat() if query.curmatfecini else None,
                'curmatfecfin': query.curmatfecfin.isoformat() if query.curmatfecfin else None
            },
            'pago': {
                'pagid': query.pagid,
                'pagmonto': query.pagmonto,
                'pagdescripcion': query.pagdescripcion,
                'pagfecreg': query.pagfecreg.isoformat() if query.pagfecreg else None,
                'pagfecha': query.pagfecha.isoformat() if query.pagfecha else None,
                'pagestado': 'Pagado' if query.pagestado == 1 else 'Pendiente' if query.pagestado == 2 else 'Sin pagar',
                'tpagnombre': query.tpagnombre,
                'pagarchivo': 'Si' if query.pagarchivo else 'No'
            }
        }

        # Llamar a la función para generar el PDF con los datos del comprobante
        return make(Report().GenerarComprobantePagoPDF(comprobante, 'admin'))
        # return make_response(jsonify(comprobante), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al generar el comprobante: {e}")
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)



def generarComprobantePagoMatricula(data):
    try:
        # Definir los alias para las tablas
        m = aliased(Matricula)
        tm = aliased(TipoMatricula)
        p = aliased(Persona)
        pa = aliased(Pago)
        tp = aliased(TipoPago)

        # Realizar la consulta para obtener el pago y la información relevante
        query = (db.session.query(
                    m.matrid, m.tipmatrid, m.matrfec, m.peridestudiante, m.pagoidmatricula, m.matrusureg, m.matrfecreg, m.matrusumod, m.matrfecmod, m.matrestado, m.matrdescripcion,
                    tm.tipmatrid, tm.tipmatrgestion, tm.tipmatrfecini, tm.tipmatrfecfin, tm.tipmatrcosto, tm.tipmatrestado, tm.tipmatrdescripcion,
                    p.pernomcompleto, p.pernrodoc, p.peremail, p.percelular,
                    pa.pagid, pa.pagmonto, pa.pagdescripcion, pa.pagfecreg, pa.pagestado, pa.pagusumod, pa.pagfecmod,
                    tp.tpagnombre, p.perfoto, pa.pagarchivo, pa.pagfecha
                )
                .join(tm, tm.tipmatrid == m.tipmatrid)
                .join(p, p.perid == m.peridestudiante)
                .join(pa, pa.pagid == m.pagoidmatricula)
                .join(tp, tp.tpagid == pa.pagtipo)
                .filter(m.matrid == data['matrid'])
                .filter(m.peridestudiante == data['perid'])
                .first())

        if not query:
            return make_response(jsonify({'error': 'No se encontraron registros para la matrícula y el estudiante.'}), HTTPStatus.NOT_FOUND)

        # Organizar los datos del comprobante
        comprobante = {
            'estudiante': {
                'pernomcompleto': query.pernomcompleto,
                'pernrodoc': query.pernrodoc,
                'peremail': query.peremail,
                'percelular': query.percelular,
                'perfoto': query.perfoto
            },
            'matricula': {
                'tipmatrid': query.tipmatrid,
                'matrfec': query.matrfec.isoformat() if query.matrfec else None,
                'matrestado': query.matrestado,
                'matrdescripcion': query.matrdescripcion,
                'tipmatrgestion': query.tipmatrgestion,
                'tipmatrfecini': query.tipmatrfecini.isoformat() if query.tipmatrfecini else None,
                'tipmatrfecfin': query.tipmatrfecfin.isoformat() if query.tipmatrfecfin else None,
                'tipmatrcosto': query.tipmatrcosto,
                'tipmatrestado': query.tipmatrestado,
                'tipmatrdescripcion': query.tipmatrdescripcion
            },
            'pago': {
                'pagid': query.pagid,
                'pagmonto': query.pagmonto,
                'pagdescripcion': query.pagdescripcion,
                'pagfecreg': query.pagfecreg.isoformat() if query.pagfecreg else None,
                'pagfecmod': query.pagfecmod.isoformat() if query.pagfecmod else None,
                'pagestado': 'Pagado' if query.pagestado == 1 else 'Pendiente' if query.pagestado == 2 else 'Sin pagar',
                'tpagnombre': query.tpagnombre,
                'pagarchivo': 'Si' if query.pagarchivo else 'No',
                'pagfecha': query.pagfecha.isoformat() if query.pagfecha else None
            }
        }

        # Llamar a la función para generar el PDF con los datos del comprobante
        return make(Report().GenerarComprobantePagoMatriculaPDF(comprobante, 'admin'))

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al generar el comprobante: {e}")
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)