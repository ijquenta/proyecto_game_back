import hashlib
from http import HTTPStatus
import os
import uuid
from core.database import select, execute, execute_function, execute_response, as_string
from psycopg2 import sql
from utils.date_formatting import *
from models.persona_model import Persona, PersonaDocAdmision, PersonaInfoAcademica, PersonaInfoMinisterial, PersonaInfoPersonal, TipoCargo, TipoProfesion, TipoEducacion
from core.config import db
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, make_response, send_file, send_from_directory


def listarPersona():
    try:
        personas = db.session.query(Persona).all()
        personas_dict = [persona.to_dict() for persona in personas]
        return make_response(jsonify(personas_dict))
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def listarPersonav2():
    listPersons = select('''
     SELECT p.perid, p.pernomcompleto, p.pernombres, p.perapepat, p.perapemat, p.pertipodoc, td.tipodocnombre, 
        p.pernrodoc, p.perfecnac, p.perdirec, p.peremail, p.percelular, p.pertelefono, p.perpais, tp.paisnombre, 
        p.perciudad, tc.ciudadnombre, p.pergenero, tg.generonombre, p.perestcivil, te.estadocivilnombre,
        p.perfoto, p.perestado, p.perobservacion, p.perusureg, p.perfecreg, p.perusumod, p.perfecmod 
        FROM academico.persona p
        left join academico.tipo_documento td on td.tipodocid = p.pertipodoc
        left join academico.tipo_pais tp on tp.paisid = p.perpais
        left join academico.tipo_ciudad tc on tc.ciudadid = p.perciudad
        left join academico.tipo_genero tg on tg.generoid = p.pergenero
        left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil    
        ORDER BY p.pernomcompleto; 
    ''')
    for person in listPersons:
        person["perfecnac"] = darFormatoFechaNacimiento(person["perfecnac"])
    #     person["perfecreg"] = darFormatoFechaConHora(person["perfecreg"])
    #     person["perfecmod"] = darFormatoFechaConHora(person["perfecmod"])

    return listPersons

def registrarPersona(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT * FROM academico.registrar_persona
                ({pernombres}, {perapepat}, {perapemat}, 
                 {pertipodoc}, {pernrodoc},  {perusureg}, {peremail} 
                )
        ''').format(
            pernombres=sql.Literal(data['pernombres']),
            perapepat=sql.Literal(data['perapepat']),
            perapemat=sql.Literal(data['perapemat']),
            pertipodoc=sql.Literal(data['pertipodoc']),
            pernrodoc=sql.Literal(data['pernrodoc']),
            perusureg=sql.Literal(data['perusureg']),
            peremail=sql.Literal(data['peremail'])
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

def eliminarPersona(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_eliminar_persona
                ({tipo},{perid},{perusumod})
        ''').format(
            tipo=sql.Literal(data['tipo']),
            perid=sql.Literal(data['perid']),
            perusumod=sql.Literal(data['perusumod'])   
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
        FROM academico.tipo_estadocivil
        order by case when estadocivilid = 1 then 0 else 1 end, estadocivilnombre;
    ''')

def tipoGenero():
    return select('''
        SELECT generoid, generonombre
        FROM academico.tipo_genero
        order by generoid;
    ''')

def tipoPais():
    return select('''
        SELECT paisid, paisnombre
        FROM academico.tipo_pais
        ORDER BY CASE WHEN paisid = 1 THEN 0 ELSE 1 END, paisnombre;
    ''')

def tipoCiudad():
    return select('''
        SELECT ciudadid, ciudadnombre, paisid
        FROM academico.tipo_ciudad;
    ''')
    
def listarUsuarios():
    listUsers = select(f'''
    SELECT id, nombre_usuario, contrasena, nombre_completo, rol
    FROM public.usuarios;
    ''')
    return listUsers


# Persona Información Personal

def listarInformacionPersonal(perid: any):
    try:
        datos = select(f''' 
                   SELECT 
                        pip.perid, 
                        pip.peredad, 
                        pip.pernrohijos, 
                        pip.perprofesion, 
                        tp.pronombre,
                        pip.perfecconversion, 
                        pip.perlugconversion, 
                        pip.perbautizoagua, 
                        pip.perbautizoespiritu, 
                        pip.pernomiglesia, 
                        pip.perdiriglesia, 
                        pip.pernompastor, 
                        pip.percelpastor,
                        pip.perexperiencia, 
                        pip.permotivo, 
                        pip.perplanesmetas,  
                        pip.perusureg, 
                        pip.perfecreg, 
                        pip.perusumod, 
                        pip.perfecmod, 
                        pip.perobservacion, 
                        pip.perestado
                   FROM academico.persona_info_personal pip
                   INNER JOIN academico.tipo_profesion tp on tp.proid = pip.perprofesion
                   WHERE pip.perid = {perid};
                   ''')
        response = {
            "status": "success",
            "data": datos
        }
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error = {
            "status": "error",
            "message": "Error in the database.",
            "details": str(e)
        }
        return make_response(jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR)

def adicionarInformacionPersonal(data):
    try:
        existe = db.session.query(PersonaInfoPersonal).filter_by(perid=data["perid"]).first()
        if existe:
            error_response = {
                "error": "Duplicate entry",
                "message": "An submenu with the same already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        infoPersonal = PersonaInfoPersonal(
            perid=data["perid"],
            peredad=data["peredad"],
            pernrohijos=data["pernrohijos"],
            perprofesion=data["perprofesion"],
            perlugconversion=data["perlugconversion"],
            perfecconversion=data["perfecconversion"],
            perbautizoagua=data["perbautizoagua"],
            perbautizoespiritu=data["perbautizoespiritu"],
            pernomiglesia=data["pernomiglesia"],
            perdiriglesia=data["perdiriglesia"],
            pernompastor=data["pernompastor"],
            percelpastor=data["percelpastor"],
            perusureg=data["perusureg"],
            perusumod=data["perusureg"],
            perfecreg=datetime.now(),
            perfecmod=datetime.now(),
            perobservacion=data["perobservacion"],
            perestado=data["perestado"],
            perexperiencia=data["perexperiencia"],
            permotivo=data["permotivo"],
            perplanesmetas=data["perplanesmetas"]
        )
        db.session.add(infoPersonal)
        db.session.commit()
        _data = infoPersonal.to_dict()

        response_data = {
            "message": "Información Personal created successfully",
            "data": _data,
            "code": HTTPStatus.OK 
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.persona_model import db, PersonaInfoPersonal
def modificarInformacionPersonal(data, perid):
    try:
        infoPersonal = PersonaInfoPersonal.query.filter_by(perid=perid).first()
        if not infoPersonal:
            error_response = {
                "error": "Not found",
                "message": f"Persona with ID {perid} not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        infoPersonal.peredad = data["peredad"]
        infoPersonal.pernrohijos = data["pernrohijos"]
        infoPersonal.perprofesion = data["perprofesion"]
        infoPersonal.perlugconversion = data["perlugconversion"]
        infoPersonal.perfecconversion = data["perfecconversion"]
        infoPersonal.perbautizoagua = data["perbautizoagua"]
        infoPersonal.perbautizoespiritu = data["perbautizoespiritu"]
        infoPersonal.pernomiglesia = data["pernomiglesia"]
        infoPersonal.perdiriglesia = data["perdiriglesia"]
        infoPersonal.pernompastor = data["pernompastor"]
        infoPersonal.percelpastor = data["percelpastor"]
        infoPersonal.perusumod = data["perusumod"]
        infoPersonal.perobservacion = data["perobservacion"]
        infoPersonal.perestado = data["perestado"]
        infoPersonal.perexperiencia = data["perexperiencia"]
        infoPersonal.permotivo = data["permotivo"]
        infoPersonal.perplanesmetas = data["perplanesmetas"]
        
        db.session.commit()
        _data = infoPersonal.to_dict()
        response_data = {
                "message": "Información Personal updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
            }
        response = make_response(jsonify(response_data), HTTPStatus.OK)
        return response
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

    
# Persona Información Académica
def listarInformacionAcademica(perid: any):
    try:
        datos = select(f'''
                   SELECT pia.perinfoaca, 
                        pia.perid, 
                        pia.pereducacion,
                        te.edunombre, 
                        pia.pernominstitucion, 
                        pia.perdirinstitucion, 
                        pia.pergescursadas, 
                        pia.perfechas, 
                        pia.pertitulo, 
                        pia.perusureg, 
                        pia.perfecreg, 
                        pia.perusumod, 
                        pia.perfecmod, 
                        pia.perobservacion, 
                        pia.perestado
                   FROM academico.persona_info_academica pia
                   JOIN academico.tipo_educacion te on te.eduid = pia.pereducacion
                   WHERE perid = {perid};
                   ''')
        response = {
            "status": "success",
            "data": datos
        }
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error = {
            "status": "error",
            "message": "Error in the database.",
            "details": str(e)
        }
        return make_response(jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def adicionarInformacionAcademica(data):
    try:
        infoAcademica = PersonaInfoAcademica(
            perid=data["perid"],
            pereducacion=data["pereducacion"],
            pernominstitucion=data["pernominstitucion"],
            perdirinstitucion=data["perdirinstitucion"],
            pergescursadas=data["pergescursadas"],
            perfechas=data["perfechas"],
            pertitulo=data["pertitulo"],
            perusureg=data["perusureg"],
            perusumod=data["perusureg"],
            perfecreg=datetime.now(),
            perfecmod=datetime.now(),
            perobservacion=data["perobservacion"],
            perestado=data["perestado"],
        )
        db.session.add(infoAcademica)
        db.session.commit()
        _data = infoAcademica.to_dict()

        response_data = {
            "message": "Información Académica created successfully",
            "data": _data,
            "code": HTTPStatus.OK 
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.persona_model import db, PersonaInfoAcademica
def modificarInformacionAcademica(data, perinfoaca):
    try:
        infoAcademica = PersonaInfoAcademica.query.filter_by(perinfoaca=perinfoaca).first()
        if not infoAcademica:
            error_response = {
                "error": "Not found",
                "message": f"Persona Información Académica with ID {perinfoaca} not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        infoAcademica.pereducacion = data["pereducacion"]
        infoAcademica.pernominstitucion = data["pernominstitucion"]
        infoAcademica.perdirinstitucion = data["perdirinstitucion"]
        infoAcademica.pergescursadas = data["pergescursadas"]
        infoAcademica.perfechas = data["perfechas"]
        infoAcademica.pertitulo = data["pertitulo"]
        infoAcademica.perusumod = data["perusumod"]
        infoAcademica.perobservacion = data["perobservacion"]
        infoAcademica.perestado = data["perestado"]

        db.session.commit()
        _data = infoAcademica.to_dict()
        response_data = {
                "message": "Información Académica updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
            }
        response = make_response(jsonify(response_data), HTTPStatus.OK)
        return response
            
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def eliminarInformacionAcademica(perinfoaca):
    try:
        infoAcademica = PersonaInfoAcademica.query.filter_by(perinfoaca=perinfoaca).first()
        if not infoAcademica:
            error_response = {
                "error": "Not found",
                "message": f"Persona Información Acadmémica with ID {perinfoaca} not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(infoAcademica)
        db.session.commit()

        response_data = {
            "message": "Información Académica deleted successfully",
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)

    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

# Persona Información Ministerial
def listarInformacionMinisterial(perid: any):
    try:
        datos = select(f'''
                   SELECT pim.perinfomin, 
                        pim.perid, 
                        pim.pernomiglesia, 
                        pim.percargo,
                        tc.carnombre, 
                        pim.pergestion, 
                        pim.perusureg,
                        pim.perfecreg,
                        pim.perusumod,
                        pim.perfecmod,
                        pim.perobservacion,
                        pim.perestado
                   FROM academico.persona_info_ministerial pim
                   INNER JOIN academico.tipo_cargo tc on tc.carid = pim.percargo
                   WHERE perid = {perid};
                   ''')
        response = {
            "status": "success",
            "data": datos
        }
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error = {
            "status": "error",
            "message": "Error in the database.",
            "details": str(e)
        }
        return make_response(jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def adicionarInformacionMinisterial(data):
    try:
        infoMinisterial = PersonaInfoMinisterial(
            perid=data["perid"],
            pernomiglesia=data["pernomiglesia"],
            percargo=data["percargo"],
            pergestion=data["pergestion"],
            perusureg=data["perusureg"],
            perusumod=data["perusureg"],
            perfecreg=datetime.now(),
            perfecmod=datetime.now(),
            perobservacion=data["perobservacion"],
            perestado=data["perestado"],
        )
        db.session.add(infoMinisterial)
        db.session.commit()
        _data = infoMinisterial.to_dict()

        response_data = {
            "message": "Información Ministerial created successfully",
            "data": _data,
            "code": HTTPStatus.OK 
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.persona_model import db, PersonaInfoMinisterial
def modificarInformacionMinisterial(data, perinfomin):      
    try:
        infoMinisterial = PersonaInfoMinisterial.query.filter_by(perinfomin=perinfomin).first()
        if not infoMinisterial:
            error_response = {
                "error": "Not found",
                "message": f"Persona with ID {perinfomin} not found.",
                "code": HTTPStatus.NOT_FOUND
            }           
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        infoMinisterial.pernomiglesia = data["pernomiglesia"]
        infoMinisterial.percargo = data["percargo"]
        infoMinisterial.pergestion = data["pergestion"]
        infoMinisterial.perusumod = data["perusumod"]
        infoMinisterial.perobservacion = data["perobservacion"]
        infoMinisterial.perestado = data["perestado"]

        db.session.commit()
        _data = infoMinisterial.to_dict()
        response_data = {
                "message": "Información Ministerial updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
            }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

# Persona Documento Admisión

def listarDocumentoAdmision(perid: any):
    print("perid", perid)
    try:
        documentos = PersonaDocAdmision.query.filter_by(perid=perid).order_by(PersonaDocAdmision.perid).all()
        _data = [documento.to_dict() for documento in documentos]

        response_data = {
            "message": "data recovered successfully",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)

    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


from werkzeug.utils import secure_filename  # Para asegurar los nombres de archivo
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

def adicionarDocumentoAdmision(data, request):
    try:
        archivos_permitidos = ['perfoto', 'perfotoci', 'perfototitulo', 'percartapastor']
        archivos = {}
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'documentoAdmision')
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Recuperar datos existentes usando perid
        documento_existente = PersonaDocAdmision.query.filter_by(perid=data['perid']).first()

        if documento_existente:
            # Verificar y eliminar archivos existentes
            for archivo_key in archivos_permitidos:
                archivo_path = getattr(documento_existente, archivo_key, None)
                if archivo_path:
                    full_path = os.path.join(upload_directory, archivo_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)

        for archivo_key in archivos_permitidos:
            if archivo_key in request.files:
                file = request.files[archivo_key]
                if file.filename == '':
                    raise ValueError(f"Nombre de archivo vacío para {archivo_key}.")
                if file and allowed_file(file.filename):
                    # Calcular hash del archivo
                    file_hash = calculate_file_hash(file)
                    filename = secure_filename(file.filename)
                    file_extension = filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{file_hash}.{file_extension}"
                    upload_path = os.path.join(upload_directory, unique_filename)

                    # Check if file already exists
                    if not os.path.exists(upload_path):
                        file.save(upload_path)
                    archivos[archivo_key] = unique_filename
                else:
                    raise ValueError(f"Tipo de archivo no permitido para {archivo_key}.")
            else:
                archivos[archivo_key] = None  # Handle case where no file is provided

        if documento_existente:
            # Update the existing record
            documento_existente.perfoto = archivos['perfoto']
            documento_existente.perfotoci = archivos['perfotoci']
            documento_existente.perfototitulo = archivos['perfototitulo']
            documento_existente.percartapastor = archivos['percartapastor']
            documento_existente.perusureg = data['perusureg']
            documento_existente.perobservacion = data['perobservacion']
            documento_existente.perestado = data['perestado']
        else:
            # Create a new entry in the database
            nuevo_documento = PersonaDocAdmision(
                perid=data['perid'],
                perfoto=archivos['perfoto'],
                perfotoci=archivos['perfotoci'],
                perfototitulo=archivos['perfototitulo'],
                percartapastor=archivos['percartapastor'],
                perusureg=data['perusureg'],
                perusumod=data['perusureg'],
                perfecreg=datetime.now(),
                perfecmod=datetime.now(),
                perobservacion=data['perobservacion'],
                perestado=data['perestado']
            )
            db.session.add(nuevo_documento)
        
        db.session.commit()

        resp = {
            "status": "success",
            "message": "Archivos subidos correctamente y datos guardados",
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
    
def mostrarDocumentoAdmision(filename):
    file_path = 'static/documentoAdmision/' + filename  
    return send_file(file_path, as_attachment=True)

def modificarDocumentoAdmision(data, request):
    try:
        archivos_permitidos = ['perfoto', 'perfotoci', 'perfototitulo', 'percartapastor']
        archivos = {}
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'documentoAdmision')
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Recuperar datos existentes usando perid
        documento_existente = PersonaDocAdmision.query.filter_by(perid=data['perid']).first()

        if not documento_existente:
            resp = {
                "status": "error",
                "message": "Documento de admisión no encontrado."
            }
            return make_response(jsonify(resp), HTTPStatus.NOT_FOUND)

        # Manejar archivos subidos
        for archivo_key in archivos_permitidos:
            if archivo_key in request.files:
                file = request.files[archivo_key]
                if file.filename == '':
                    raise ValueError(f"Nombre de archivo vacío para {archivo_key}.")
                if file and allowed_file(file.filename):
                    # Calcular hash del archivo
                    file_hash = calculate_file_hash(file)
                    filename = secure_filename(file.filename)
                    file_extension = filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{file_hash}.{file_extension}"
                    upload_path = os.path.join(upload_directory, unique_filename)

                    # Check if file already exists
                    if not os.path.exists(upload_path):
                        file.save(upload_path)

                    # Guardar la nueva ruta del archivo y eliminar el anterior
                    archivo_path = getattr(documento_existente, archivo_key, None)
                    if archivo_path:
                        full_path = os.path.join(upload_directory, archivo_path)
                        if os.path.exists(full_path)        :
                            os.remove(full_path)

                    archivos[archivo_key] = unique_filename
                else:
                    raise ValueError(f"Tipo de archivo no permitido para {archivo_key}.")
            else:
                archivos[archivo_key] = getattr(documento_existente, archivo_key)  # Mantener archivo existente

        # Actualizar el registro existente
        documento_existente.perfoto = archivos['perfoto']
        documento_existente.perfotoci = archivos['perfotoci']
        documento_existente.perfototitulo = archivos['perfototitulo']
        documento_existente.percartapastor = archivos['percartapastor']
        documento_existente.perusumod = data['perusumod']
        documento_existente.perfecmod = datetime.now()
        documento_existente.perobservacion = data['perobservacion']
        documento_existente.perestado = data['perestado']                       

        db.session.commit()

        resp = {
            "status": "success",
            "message": "Documento de admisión actualizado correctamente.",
            "filenames": {k: v for k, v in archivos.items() if v}
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al modificar el documento de admisión: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)
    
# Tipo Profesion
def listarTipoProfesion():
    try:
        tipoProfesiones = TipoProfesion.query.order_by(TipoProfesion.pronombre).all()
        _data = [tipoProfesion.to_dict() for tipoProfesion in tipoProfesiones]
       
        response_data = {
            "message": "data recovered successfully",
            "data": _data,
            "code": HTTPStatus.OK 
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def adicionarTipoProfesion(data):
    try:
        existe = db.session.query(TipoProfesion).filter_by(pronombre=data["pronombre"]).first()
        if existe:
            error_response = {
                "error": "Duplicate entry",
                "message": "An submenu with the same already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        tipoProfesion = TipoProfesion(
            pronombre=data["pronombre"],
            prousureg=data["prousureg"],
            prousumod=data["prousureg"],
            profecreg=datetime.now(),
            profecmod=datetime.now(),
            proestado=data["proestado"],
            proobservacion=data["proobservacion"],
        )
        db.session.add(tipoProfesion)
        db.session.commit()
        _data = tipoProfesion.to_dict()

        response_data = {
            "message": "Tipo de Profesión created successfully",
            "data": _data,
            "code": HTTPStatus.OK
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.persona_model import db, TipoProfesion

def modificarTipoProfesion(data, proid):
    try:
        tipoProfesion = TipoProfesion.query.filter_by(proid=proid).first()
        if not tipoProfesion:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        tipoProfesion.pronombre = data["pronombre"]
        tipoProfesion.prousumod = data["prousumod"]
        tipoProfesion.profecmod = datetime.now()
        tipoProfesion.proestado = data["proestado"]
        tipoProfesion.proobservacion = data["proobservacion"]

        db.session.commit()
        _data = tipoProfesion.to_dict()
        response_data = {
                "message": "Tipo de Profesión updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
            }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def eliminarTipoProfesion(proid):
    try:
        tipoProfesion = TipoProfesion.query.filter_by(proid=proid).first()
        if not tipoProfesion:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(tipoProfesion)
        db.session.commit()
        response_data = {
            "message": "Tipo de Profesión deleted successfully",
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
# Tipo Educación
def listarTipoEducacion():
    try:
        tipoEducaciones = TipoEducacion.query.order_by(TipoEducacion.edunombre).all()
        _data = [tipoEducacion.to_dict  () for tipoEducacion in tipoEducaciones]
        
        response_data = {
            "message": "data recovered successfully",
            "data": _data,
            "code": HTTPStatus.OK 
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def adicionarTipoEducacion(data):
    try:
        existe = db.session.query(TipoEducacion).filter_by(edunombre=data["edunombre"]).first()
        if existe:
            error_response = {
                "error": "Duplicate entry",
                "message": "An submenu with the same already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        tipoEducacion = TipoEducacion(
            edunombre = data["edunombre"],
            eduusureg=data["eduusureg"],
            eduusumod=data["eduusureg"],
            edufecreg=datetime.now(),
            edufecmod=datetime.now(),
            eduestado=data["eduestado"],
            eduobservacion=data["eduobservacion"],
        )

        db.session.add(tipoEducacion)
        db.session.commit()
        _data = tipoEducacion.to_dict()

        response_data = {
            "message": "Tipo de Educación created successfully",
            "data": _data,
            "code": HTTPStatus.OK
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.persona_model import db, TipoEducacion
def modificarTipoEducacion(data, eduid):
    try:
        tipoEducacion = TipoEducacion.query.filter_by(eduid=eduid).first()
        if not tipoEducacion:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        tipoEducacion.edunombre = data["edunombre"]
        tipoEducacion.eduusumod = data["eduusumod"]
        tipoEducacion.edufecmod = datetime.now()
        tipoEducacion.eduestado = data["eduestado"]
        tipoEducacion.eduobservacion = data["eduobservacion"]

        db.session.commit()
        _data = tipoEducacion.to_dict()
        response_data = {
                "message": "Tipo de Educación updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
            }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
 
def eliminarTipoEducacion(eduid):
    try:
        tipoEducacion = TipoEducacion.query.filter_by(eduid=eduid).first()
        if not tipoEducacion:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(tipoEducacion)
        db.session.commit()
        response_data = {
            "message": "Tipo de Educación deleted successfully",
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
  
# Tipo Cargo
def listarTipoCargo():
    try:
        tipoCargos = TipoCargo.query.order_by(TipoCargo.carnombre).all()
        _data = [tipoCargo.to_dict() for tipoCargo in tipoCargos]

        response_data = {
            "message": "data recovered successfully",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)

    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def adicionarTipoCargo(data):
    try:
        existe = db.session.query(TipoCargo).filter_by(carnombre=data["carnombre"]).first()
        if existe:
            error_response = {
                "error": "Duplicate entry",
                "message": "An submenu with the same already exists."
            }
            return make_response(jsonify(error_response), HTTPStatus.CONFLICT)

        tipoCargo = TipoCargo(
            carnombre = data["carnombre"],
            carusureg=data["carusureg"],
            carusumod=data["carusureg"],
            carfecreg=datetime.now(),
            carfecmod=datetime.now(),
            carestado=data["carestado"],
            carobservacion=data["carobservacion"],
        )
    
        db.session.add(tipoCargo)
        db.session.commit()
        _data = tipoCargo.to_dict()
    
        response_data = {
            "message": "Tipo de Cargo created successfully",
            "data": _data,
            "code": HTTPStatus.OK
        }
    
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
    
        return response
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.persona_model import db, TipoCargo
def modificarTipoCargo(data, carid):
    try:
        tipoCargo = TipoCargo.query.filter_by(carid=carid).first()
        if not tipoCargo:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        tipoCargo.carnombre = data["carnombre"]
        tipoCargo.carusumod = data["carusumod"]
        tipoCargo.carfecmod = datetime.now()
        tipoCargo.carestado = data["carestado"]
        tipoCargo.carobservacion = data["carobservacion"]

        db.session.commit()
        _data = tipoCargo.to_dict()
        response_data = {
                "message": "Tipo de Cargo updated successfully",
                "data": _data,
                "code": HTTPStatus.OK
        }
        response = make_response(jsonify(response_data), HTTPStatus.CREATED)
        return response
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def eliminarTipoCargo(carid):
    try:
        tipoCargo = TipoCargo.query.filter_by(carid=carid).first()
        if not tipoCargo:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(tipoCargo)
        db.session.commit()
        response_data = {
            "message": "Tipo de Cargo deleted successfully",
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)

    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)