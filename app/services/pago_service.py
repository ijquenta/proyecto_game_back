from http import HTTPStatus
from core.database import select, execute_function
from flask import jsonify, make_response
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

def manage_pago(data):
    tipo = data.get('tipo')
    if tipo == 1:
        return create_pago(data)
    elif tipo == 2:
        return update_pago(data)
    elif tipo == 3:
        return delete_pago(data)
    else:
        return {"status": "error", "message": "Tipo de operación no soportada."}, HTTPStatus.BAD_REQUEST

from models.inscripcion_model import Inscripcion, db
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
                    i.pagid, m.matrid, tm.tipmatrgestion, c.curnombre, m2.matnombre, p2.pernomcompleto, 
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
