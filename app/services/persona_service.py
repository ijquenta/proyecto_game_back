import os  # Para manejo del sistema de archivos
import hashlib  # Para manejo de hashes
from datetime import datetime  # Para manejo de fechas y tiempos
from http import HTTPStatus  # Para códigos de estado HTTP estándar

from flask import jsonify, make_response, send_file, send_from_directory  # Para respuestas HTTP y manejo de archivos
from werkzeug.utils import secure_filename  # Para asegurar nombres de archivos subidos
from sqlalchemy.exc import SQLAlchemyError  # Para manejo de errores de SQLAlchemy

from core.config import db  # Configuración de la base de datos
from core.database import select, execute, execute_function, execute_response, as_string  # Funciones de base de datos personalizadas
from models.persona_model import *  # Modelo de la entidad Persona
from utils.date_formatting import *  # Funciones de formateo de fechas
from psycopg2 import sql # Para realizar consultas a la base de datos

    # Registrar persona desde el formulario register, con retorno del perid
def createPersonForm(data):
    if not data:
        return make_response(jsonify({'message': 'No hay datos disponibles'}), HTTPStatus.BAD_REQUEST)

    try:
        persona = Persona(
            pernomcompleto=data.get('perapepat') + ' ' + data.get('perapemat') + ' ' + data.get('pernombres'),
            pernombres=data.get('pernombres'),
            perapepat=data.get('perapepat'),
            perapemat=data.get('perapemat'),
            pertipodoc=data.get('pertipodoc'),
            pernrodoc=data.get('pernrodoc'),
            peremail=data.get('peremail'),
            perusureg=data.get('perusureg'),
            perusumod=data.get('perusureg'),
            perfecreg=datetime.now(),
            perfecmod=datetime.now(),
            perestado=1,
            perobservacion=data.get('perobservacion')
        )
        db.session.add(persona)
        db.session.commit()

        resp = {
            "status": "success",
            "message": "La persona se ha creado correctamente.",
            "perid": persona.perid
        }
        
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        print(e)
        return make_response(jsonify({'message': f'Error: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR)      

# Section Person 

def getPersons():
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
    
# Manage person for create or update
def managePerson(data, request):
    if data['tipo'] == 1:
        return createPerson(data, request)
    elif data['tipo'] == 2: 
        return updatePerson(data, request)
    elif data['tipo'] == 3:
        return deletePerson(data)
    else:
        return make_response(jsonify({"status": "error", "message": "Tipo de operación no soportada."}), HTTPStatus.BAD_REQUEST)

# Create a new person
def createPerson(data, request):
    try:
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'personProfilePhoto')
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Manage uploaded files
        files = handle_uploaded_files(request, upload_directory)

        # Create a new person record
        persona = Persona(       
            perfoto=files['perfoto'],
            pernomcompleto=f"{data['perapepat']} {data['perapemat']} {data['pernombres']}",
            perapepat=data["perapepat"],
            perapemat=data["perapemat"],
            pernombres=data["pernombres"],
            pertipodoc=data["pertipodoc"],
            pernrodoc=data["pernrodoc"],
            perfecnac=formatDateBirth(data["perfecnac"]),
            perdirec=data["perdirec"],
            peremail=data["peremail"],
            percelular=data["percelular"],
            pertelefono=data["pertelefono"],
            perpais=data["perpais"],
            perciudad=data["perciudad"],
            pergenero=data["pergenero"],
            perestcivil=data["perestcivil"],
            perusumod=data["perusumod"],
            perfecmod=datetime.now(),
            perobservacion=data["perobservacion"],
            perestado=data["perestado"]
        )

        db.session.add(persona)
        db.session.commit()

        resp = {
            "status": "success",
            "message": "El perfil de la persona se ha creado correctamente.",
            "perfoto": {k: v for k, v in files.items() if v}
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al crear el perfil de la persona: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

# Update a person
def updatePerson(data, request):
    try:
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'personProfilePhoto')
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Recover existing data using perid
        persona = Persona.query.filter_by(perid=data['perid']).first()
        if not persona:
            resp = {
                "status": "error",
                "message": "Persona no encontrada."
            }
            return make_response(jsonify(resp), HTTPStatus.NOT_FOUND)

        # Manage uploaded files
        files = handle_uploaded_files(request, upload_directory)

        # Actualiza el registro existente
        persona.perfoto = files['perfoto'] or persona.perfoto
        persona.pernomcompleto = f"{data['perapepat']} {data['perapemat']} {data['pernombres']}"
        persona.perapepat = data["perapepat"]
        persona.perapemat = data["perapemat"]
        persona.pernombres = data["pernombres"]
        persona.pertipodoc = data["pertipodoc"]
        persona.pernrodoc = data["pernrodoc"]
        persona.perfecnac = formatDateBirth(data["perfecnac"])
        persona.perdirec = data["perdirec"]
        persona.peremail = data["peremail"]
        persona.percelular = data["percelular"]
        persona.pertelefono = data["pertelefono"]
        persona.perpais = data["perpais"]
        persona.perciudad = data["perciudad"]
        persona.pergenero = data["pergenero"]
        persona.perestcivil = data["perestcivil"]
        persona.perusumod = data["perusumod"]
        persona.perfecmod = datetime.now()
        persona.perobservacion=data["perobservacion"]
        persona.perestado=data["perestado"]
        
        db.session.commit()

        resp = {
            "status": "success",
            "message": "El perfil de la persona se ha actualizado correctamente.",
            "perfoto": {k: v for k, v in files.items() if v}
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al actualizar el perfil de la persona: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

def deletePerson(data):
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

def deletePersonForm(perid):
    try:
        persona = Persona.query.filter_by(perid=perid).first()
        if not persona:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        db.session.delete(persona)
        db.session.commit()
        response_data = {
            "message": "Person deleted successfully",
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

# Section profile    
# Manage profile
from models.persona_model import Persona # Import person model 
def updateProfile(data, request):
    try:
        archivo_perfil = ['perfoto']
        archivos = {}
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, '..', 'static', 'personProfilePhoto')
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # Recover existing data using perid
        persona = Persona.query.filter_by(perid=data['perid']).first()

        if not persona:
            resp = {
                "status": "error",
                "message": "Persona no encontrado."
            }
            return make_response(jsonify(resp), HTTPStatus.NOT_FOUND)

        # Manage uploaded files
        for archivo in archivo_perfil:
            if archivo in request.files:
                file = request.files[archivo]
                if file.filename == '':
                    raise ValueError(f"Nombre de archivo vacío para {archivo}.")
                if file and allowed_file(file.filename):

                    file_hash = calculate_file_hash(file)
                    filename = secure_filename(file.filename)
                    file_extension = filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{file_hash}.{file_extension}"
                    upload_path = os.path.join(upload_directory, unique_filename)

                    # Verify that the file already exists
                    if not os.path.exists(upload_path):
                        file.save(upload_path)

                    # Save the new file path and delete the old one
                    archivo_path = getattr(persona, archivo, None)
                    if archivo_path:
                        full_path = os.path.join(upload_directory, archivo_path)
                        if os.path.exists(full_path)        :
                            os.remove(full_path)

                    archivos[archivo] = unique_filename
                else:
                    raise ValueError(f"Tipo de archivo no permitido para {archivo}.")
            else:
                archivos[archivo] = getattr(persona, archivo)  # Keep existing file

        # Update existing record
        persona.perfoto = archivos['perfoto']
        persona.pernomcompleto = data["perapepat"] + " " + data["perapemat"] + " " + data["pernombres"]
        persona.perapepat = data["perapepat"]
        persona.perapemat = data["perapemat"]
        persona.pernombres = data["pernombres"]
        persona.pertipodoc = data["pertipodoc"]
        persona.pernrodoc = data["pernrodoc"]
        persona.perfecnac = formatDateBirth(data["perfecnac"])
        persona.perdirec = data["perdirec"]
        persona.peremail = data["peremail"]
        persona.percelular = data["percelular"]
        persona.pertelefono = data["pertelefono"]
        persona.perpais = data["perpais"]
        persona.perciudad = data["perciudad"]
        persona.pergenero = data["pergenero"]
        persona.perestcivil = data["perestcivil"]
        persona.perusumod = data["perusumod"]
        persona.perfecmod = datetime.now()
        
        db.session.commit()

        resp = {
            "status": "success",
            "message": "El perfil de la persona se ha actualizado correctamente.",
            "perfoto": {k: v for k, v in archivos.items() if v}
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al modificar el documento de admisión: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)

# Show person for profile
def showPersonData(perid):
    try:
        persona = Persona.query.filter_by(perid=perid).first()
        if not persona:
            error_response = {
                "error": "Not found",
                "message": "The specified resource was not found.",
                "code": HTTPStatus.NOT_FOUND
            }
            return make_response(jsonify(error_response), HTTPStatus.NOT_FOUND)

        _data = persona.to_dict()
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
    

# Types
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

def getUsers():
    listUsers = select(f'''
    SELECT usuname
    FROM academico.usuario;
    ''')                                                        
    return listUsers

# Other fuctions 
    
from models.persona_model import db, Persona  # Import person model
# Handle uploaded files in manage person
def handle_uploaded_files(request, upload_directory):
    profilePhotoFile = ['perfoto']
    files = {}

    for archivo in profilePhotoFile:
        if archivo in request.files:
            file = request.files[archivo]
            if file.filename == '':
                raise ValueError(f"Nombre de archivo vacío para {archivo}.")
            if file and allowed_file(file.filename):
                file_hash = calculate_file_hash(file)
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{file_hash}.{file_extension}"
                upload_path = os.path.join(upload_directory, unique_filename)

                # Verify that the file does not exist
                if not os.path.exists(upload_path):
                    file.save(upload_path)

                files[archivo] = unique_filename
            else:
                raise ValueError(f"Tipo de archivo no permitido para {archivo}.")
        else:
            files[archivo] = None  # There is no file uploaded for this field

    return files

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