<<<<<<< HEAD
from flask import jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus

from models.game_model import Usuario
from models.game_model import Paciente
from models.game_model import Doctor
from models.game_model import Sesion

from http import HTTPStatus

from flask import jsonify, make_response

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy import case
from datetime import datetime
from core.database import db, select, execute_function

# Usuarios
def obtenerUsuarios():
    try:
        usuarios = Usuario.query.order_by(Usuario.nombre).all()
        response = [usuario.to_dict() for usuario in usuarios]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.", 
=======
# Librerías de Flask y Werkzeug
from flask import make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Librerías de PostgreSQL y SQLAlchemy
from psycopg2 import sql
from sqlalchemy import or_

# Modelos de la aplicación
from models.persona_model import Persona
from models.rol_model import Rol

# Recursos y servicios
from resources.Autenticacion import TokenGenerator
from services.email_service import EmailService

# Utilidades y funciones auxiliares
from utils.date_formatting import *
from core.database import select, execute, as_string

from sqlalchemy.exc import SQLAlchemyError  # Para manejo de errores de SQLAlchemy
from http import HTTPStatus  # Para códigos de estado HTTP estándar

class UsuarioService:
    def __init__(self, mail):
        self.email_service = EmailService(mail)

    def request_password_reset(self, data):
        user = Usuario.query.filter_by(usuname=data['usuname'], usuemail=data['usuemail']).first()
        if user:
            token = TokenGenerator.generate_confirmation_token(user.usuid, user.rolid)
            self.email_service.send_reset_email(user.usuemail, token)
            return {"message": "A password reset email has been sent.", "code": 200}, 200
        return {"message": "User not found."}, 404          

    def reset_password(self, token, new_password):
        try:
            payload = TokenGenerator.confirm_token(token)
            if not payload:
                return {"message": "Invalid or expired token."}, 400
            user_id = payload['usuid']
            user = Usuario.query.get(user_id)
            if user:
                user.usupassword = generate_password_hash(new_password)
                db.session.commit()
                return {"message": "Password has been reset."}, 200
            return {"message": "User not found."}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    def change_password(self, user_id, old_password, new_password):
        user = Usuario.query.get(user_id)
        if not user or not check_password_hash(user.usupassword, old_password):
            return {"message": "Old password is incorrect."}, 400
        user.usupassword = generate_password_hash(new_password)
        db.session.commit()
        return {"message": "Password has been changed."}, 200

# Gestionar Usuario
def gestionarUsuario(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_gestionar_usuario(
                        {tipo}, {usuid}, {perid}, {rolid}, {usuname}, {usupassword}, {usupasswordhash}, 
                        {usuemail}, {usudescripcion}, {usuestado}, {usuusureg});
            ''').format( tipo=sql.Literal(data['tipo']), 
                         usuid=sql.Literal(data['usuid']), 
                         perid=sql.Literal(data['perid']), 
                         rolid=sql.Literal(data['rolid']), 
                         usuname=sql.Literal(data['usuname']), 
                         usupassword = sql.Literal(generate_password_hash(data['usupassword'])),
                         usupasswordhash= sql.Literal(generate_password_hash(data['usupassword'])), 
                         usuemail=sql.Literal(data['usuemail']), 
                         usudescripcion=sql.Literal(data['usudescripcion']), 
                         usuestado=sql.Literal(data['usuestado']), 
                         usuusureg=sql.Literal(data['usuusureg']))
        result = execute(as_string(query))
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

# Gestionar Usuario Estado
def gestionarUsuarioEstado(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_usuario_gestionar_estado({tipo}, {usuid}, {usuusumod});
            ''').format( tipo=sql.Literal(data['tipo']), usuid=sql.Literal(data['usuid']), usuusumod=sql.Literal(data['usuusumod']))
        result = execute(as_string(query))
    except Exception as err:
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

# Gestionar Usuario Password(Contraseña)
def gestionarUsuarioPassword(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_usuario_password({usuid}, {usupassword}, {usuusumod});
            ''').format( usuid=sql.Literal(data['usuid']), usupassword = sql.Literal(generate_password_hash(data['usupassword'])), usuusumod=sql.Literal(data['usuusumod']))
        result = execute(as_string(query))
    except Exception as err:
        return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

# Lista de Usuarios
def listaUsuario():
    try:
        users = db.session.query(Usuario2).all()
        users_dict = [user.to_dict() for user in users]
        return make_response(jsonify(users_dict))
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)  
    
def listaUsuariov2():
    result = select(f'''
        SELECT 
        u.usuid, u.perid, p.pernomcompleto, p.pernrodoc, p.perfoto, u.rolid, r.rolnombre, u.usuname, 
        u.usuemail, u.usudescripcion, 
        u.usuestado, u.usuusureg, u.usufecreg, u.usuusumod, u.usufecmod
        FROM academico.usuario u
        inner join academico.persona p on p.perid = u.perid
        inner join academico.rol r on r.rolid = u.rolid         
        order by p.pernomcompleto 
    ''')    
    return result
    
def tipoPersona():
    return select(f''' 
    select perid, pernomcompleto, pernrodoc, perfoto from academico.persona p 
    where perestado = 1
    order by pernomcompleto;
    ''')
    
def tipoPersonaDocente():
    return select(f'''
    select p.perid, p.pernomcompleto, p.pernrodoc, p.perfoto 
    from academico.persona p, academico.usuario u
    where perestado = 1 and u.perid = p.perid and u.rolid = 3
    order by p.pernomcompleto;
    ''')

def perfil(data):
    return select(f'''
    SELECT u.usuid, u.perid, p.pernomcompleto, p.perfoto, u.rolid, r.rolnombre , u.usuname, u.usuemail 
    FROM academico.usuario u
    left join academico.persona p on p.perid = u.perid
    left join academico.rol r on r.rolid = u.rolid 
    where u.usuid ={data['usuid']};
    ''')

def listarRoles():
    return select(f'''
    SELECT rolid, rolnombre, roldescripcion, rolusureg, rolfecreg, rolusumod, rolfecmod, rolestado
    FROM academico.rol
    where rolestado = 1
    order by rolid;        
    ''')




from models.usuario_model import Usuario2
def listarPacientes(): 
    """
    try:
        pacientes = Paciente.query.order_by(Paciente.id).all()
        _data = [paciente.to_dict() for paciente in pacientes]
       
        response_data = {
            "message": "Pacientes, OK",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
<<<<<<< HEAD

# Pacientes
def obtenerPacientes():
    try:
        pacientes = Paciente.query.order_by(Paciente.id_paciente).all()
        response = [paciente.to_dict() for paciente in pacientes]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.",
=======
    """
from models.usuario_model import Usuario2

def listarProgresos():
    """
    try:
        # Consulta a la base de datos para obtener todos los registros de la tabla Progreso
        progresos = Progreso.query.order_by(Progreso.id).all()
        
        # Convertir cada objeto Progreso en un diccionario
        _data = [progreso.to_dict() for progreso in progresos]
        
        # Construir la respuesta exitosa
        response_data = {
            "message": "Progresos, OK",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        # Construir la respuesta en caso de error en la base de datos
        error_response = {
            "error": "Error in the database.",
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
<<<<<<< HEAD
    
    
# Doctores
def obtenerDoctores():
    try:
        doctores = Doctor.query.order_by(Doctor.id_doctor).all()
        response = [doctor.to_dict() for doctor in doctores]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
  
def obtenerSesiones():
    try:
        sesiones = Sesion.query.order_by(Sesion.id_session).all()
        response = [sesion.to_dict() for sesion in sesiones]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def crearUsuario(data):
    try:
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            numero_carnet=data['numero_carnet'],
            telefono=data['telefono'],
            fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date() if data.get('fecha_nacimiento') else None,
            rol=data['rol']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return make_response(jsonify({'message': 'Usuario creado correctamente'}), HTTPStatus.CREATED)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

    
def crearPaciente(data):
    try:
        nuevo_paciente = Paciente(
            id_usuario=data['id_usuario'],
            diagnostico=data.get('diagnostico'),
            rango_movimiento=data.get('rango_movimiento'),
            fuerza=data.get('fuerza'),
            estabilidad=data.get('estabilidad'),
            descripcion=data.get('descripcion'),
            observacion=data.get('observacion')
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
        return make_response (jsonify({'message': 'Paciente creado correctamente'}), HTTPStatus.CREATED)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

def crearDoctor(data):
    try:
        nuevo_doctor = Doctor(
            id_usuario=data['id_usuario'],
            especialidad=data.get('especialidad')
        )
        db.session.add(nuevo_doctor)
        db.session.commit()
        return make_response(jsonify({'message': 'Doctor creado correctamente'}), HTTPStatus.CREATED)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

def crearSesion(data):
    try:
        nueva_sesion = Sesion(
            id_paciente=data['id_paciente'],
            id_doctor=data['id_doctor'],
            tiempo_sesion=data.get('tiempo_sesion'),
            puntaje_obtenido=data.get('puntaje_obtenido'),
            descripcion=data.get('descripcion'),
            observaciones=data.get('observaciones'),
            ejercicios_realizados=data.get('ejercicios_realizados'),
            nivel_dificultad=data['nivel_dificultad'],
            estado_emocional=data['estado_emocional']
        )
        db.session.add(nueva_sesion)
        db.session.commit()
        return make_response(jsonify({'message': 'Sesión creada correctamente'}), HTTPStatus.CREATED)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.game_model import db, Usuario
def modificarUsuario(data, usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.nombre = data.get('nombre', usuario.nombre)
            usuario.apellido = data.get('apellido', usuario.apellido)
            usuario.email = data.get('email', usuario.email)
            usuario.numero_carnet = data.get('numero_carnet', usuario.numero_carnet)
            usuario.telefono = data.get('telefono', usuario.telefono)
            usuario.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date() if data.get('fecha_nacimiento') else usuario.fecha_nacimiento
            usuario.rol = data.get('rol', usuario.rol)
            db.session.commit()
            return make_response(jsonify({'message': 'Usuario actualizado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
    
from models.game_model import db, Paciente
def modificarPaciente(data, paciente_id):
    try:
        paciente = Paciente.query.get(paciente_id)
        if paciente:
            paciente.diagnostico = data.get('diagnostico', paciente.diagnostico)
            paciente.rango_movimiento = data.get('rango_movimiento', paciente.rango_movimiento)
            paciente.fuerza = data.get('fuerza', paciente.fuerza)
            paciente.estabilidad = data.get('estabilidad', paciente.estabilidad)
            paciente.descripcion = data.get('descripcion', paciente.descripcion)
            paciente.observacion = data.get('observacion', paciente.observacion)
            db.session.commit()
            return make_response(jsonify({'message': 'Paciente actualizado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Paciente no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.game_model import db, Doctor
def modificarDoctor(data, doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            doctor.especialidad = data.get('especialidad', doctor.especialidad)
            db.session.commit()
            return make_response(jsonify({'message': 'Doctor actualizado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Doctor no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.game_model import db, Sesion
def modificarSesion(data , sesion_id):
    try:
        sesion = Sesion.query.get(sesion_id)
        if sesion:
            sesion.tiempo_sesion = data.get('tiempo_sesion', sesion.tiempo_sesion)
            sesion.puntaje_obtenido = data.get('puntaje_obtenido', sesion.puntaje_obtenido)
            sesion.descripcion = data.get('descripcion', sesion.descripcion)
            sesion.observaciones = data.get('observaciones', sesion.observaciones)
            sesion.ejercicios_realizados = data.get('ejercicios_realizados', sesion.ejercicios_realizados)
            sesion.nivel_dificultad = data.get('nivel_dificultad', sesion.nivel_dificultad)
            sesion.estado_emocional = data.get('estado_emocional', sesion.estado_emocional)
            db.session.commit()
            return make_response(jsonify({'message': 'Sesión actualizada correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Sesión no encontrada'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)


from models.game_model import db, Usuario
def desactivarUsuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.estado = 'inactivo'
            db.session.commit()
            return make_response(jsonify({'message': 'Usuario desactivado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.game_model import db, Paciente
def desactivarPaciente(paciente_id):
    try:
        paciente = Paciente.query.get(paciente_id)
        if paciente:
            paciente.estado = 'inactivo'
            db.session.commit()
            return make_response(jsonify({'message': 'Paciente desactivado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Paciente no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.game_model import db, Doctor
def desactivarDoctor(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            doctor.estado = 'inactivo'
            db.session.commit()
            return make_response(jsonify({'message': 'Doctor desactivado correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Doctor no encontrado'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)

from models.game_model import db, Sesion
def desactivarSesion(sesion_id):
    try:
        sesion = Sesion.query.get(sesion_id)
        if sesion:
            sesion.estado = 'inactivo'
            db.session.commit()
            return make_response(jsonify({'message': 'Sesión desactivada correctamente'}), HTTPStatus.OK)
        else:
            return make_response(jsonify({'error': 'Sesión no encontrada'}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
=======
    """

    
def crearRol(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT * from academico.agregarrol({rolNombre}, {rolDescripcion}, {rolUsuReg});
            ''').format( rolNombre=sql.Literal(data['rolNombre']), rolDescripcion=sql.Literal(data['rolDescripcion']), rolUsuReg=sql.Literal(data['rolUsuReg']))
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
            ''').format( rolId=sql.Literal(data['rolId']), rolNombre=sql.Literal(data['rolNombre']), rolDescripcion=sql.Literal(data['rolDescripcion']), rolUsuMod=sql.Literal(data['rolUsuMod']))
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
            ''').format(rolid=sql.Literal(data['rolid']),rolusumod=sql.Literal(data['rolusumod']))
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
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def obtenerEmail(data):
    res = select(f'''
    select usuid, usuname, usuemail from academico.usuario u where usuname = \'{data['usuname']}\' and usuemail = \'{data['usuemail']}\'
    ''')
    return res

# search User for name or email
def buscarUsuario(data):
    usuariosEncontrados = Usuario.query.join(
        Rol, Usuario.rolid == Rol.rolid).join(Persona, Usuario.perid == Persona.perid).filter(
        or_(Usuario.usuname == data.get('usuname'), 
            Usuario.usuemail == data.get('usuemail')
        )).all()
    
    _data = [usuario.to_dict_with_persona_rol() for usuario in usuariosEncontrados] if usuariosEncontrados else None
    
    data_response = {
        "message": "Usuario encontrado" if _data else "Usuario no encontrado",
        "data": _data if _data else [],
        "code": 200 if _data else 404
    } 
    return make_response(jsonify(data_response), data_response["code"])
    
# Reset Password in "Forgot password"
def resetPassword(token, data):
    # Verificar si el token es válido
    usuid = TokenGenerator.confirm_token(token)
    if not usuid:
        return {'message': 'The reset link is invalid or has expired.'}, 400
    
    # Buscar al usuario por su id
    user = Usuario.query.filter_by(usuid=usuid).first()
    if user:
        try:
            # Generar el hash de la nueva contraseña
            hashed_password = generate_password_hash(data['usupassword'])
            
            # Actualizar los campos de la contraseña y de modificación
            user.usupassword = hashed_password
            user.usuusumod = data['usuname']
            user.usufecmod = datetime.now()

            # Guardar los cambios en la base de datos
            db.session.commit()

            return {'message': 'Your password has been updated successfully!'}, 200
        
        except Exception as err:
            print(err)
            return {'code': 0, 'message': 'Error: ' + str(err)}, 500

    return {'message': 'User not found.'}, 404

# Change Password of the user panel
from models.usuario_model import Usuario2, db
def changePassword(data):
    # Buscar al usuario por su nombre de usuario
    user = Usuario.query.filter_by(usuname=data['usuname']).first()
    
    if user:
        try:
            # Generar el hash de la nueva contraseña
            hashed_password = generate_password_hash(data['usupassword'])
            
            # Actualizar los campos de la contraseña y de modificación
            user.usupassword = hashed_password
            user.usuusumod = data['usuname']
            user.usufecmod = datetime.now()

            # Guardar los cambios en la base de datos
            db.session.commit()

            return {'message': 'Your password has been updated successfully!'}, 200
        
        except Exception as err:
            print(err)
            return {'code': 0, 'message': 'Error: ' + str(err)}, 500

    return {'message': 'User not found.'}, 404
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
