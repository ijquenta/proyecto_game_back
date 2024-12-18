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
from sqlalchemy.orm import joinedload

# Usuarios
def obtenerUsuarios():
    try:
        usuarios = Usuario.query.order_by(Usuario.nombre).all()
        response = [usuario.to_dict() for usuario in usuarios]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.", 
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)
    
def obtenerUsuarioPorId(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            return make_response(jsonify(usuario.to_dict()), HTTPStatus.OK)
        else:
            return make_response(jsonify({"error": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def obtenerPacientes():
    try:
        pacientes = Paciente.query.options(
            joinedload(Paciente.usuario)  # Eager load the related Usuario
        ).order_by(Paciente.id_paciente).all()
        
        response = []
        for paciente in pacientes:
            paciente_dict = paciente.to_dict()
            # Add the related usuario information
            paciente_dict['usuario'] = paciente.usuario.to_dict() if paciente.usuario else None
            response.append(paciente_dict)
        
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error en la base de datos.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)

def obtenerDoctores():
    try:
        doctores = Doctor.query.options(
            joinedload(Doctor.usuario)  # Eager load the related Usuario
        ).order_by(Doctor.id_doctor).all()
        
        response = []
        for doctor in doctores:
            doctor_dict = doctor.to_dict()
            # Add the related usuario information
            doctor_dict['usuario'] = doctor.usuario.to_dict() if doctor.usuario else None
            response.append(doctor_dict)
        
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
        sesiones = Sesion.query.options(
            joinedload(Sesion.paciente),  # Eager load the related Paciente
            joinedload(Sesion.doctor)     # Eager load the related Doctor
        ).order_by(Sesion.id_session).all()
        
        response = []
        for sesion in sesiones:
            sesion_dict = sesion.to_dict()
            # Add the related paciente and doctor information
            sesion_dict['paciente'] = sesion.paciente.to_dict() if sesion.paciente else None
            sesion_dict['doctor'] = sesion.doctor.to_dict() if sesion.doctor else None
            
            # Optional: Add usuario information for paciente and doctor
            if sesion_dict['paciente']:
                sesion_dict['paciente']['usuario'] = sesion.paciente.usuario.to_dict() if sesion.paciente.usuario else None
            
            if sesion_dict['doctor']:
                sesion_dict['doctor']['usuario'] = sesion.doctor.usuario.to_dict() if sesion.doctor.usuario else None
            
            response.append(sesion_dict)
        
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
            estado_emocional=data['estado_emocional'],
            mejoras_observadas=data['mejoras_observadas'],
            feedback=data['feedback'],
            notas=data['notas'],
            resultados_prueba=data['resultados_prueba'],
            estado=data['estado'],
            fecha_sesion=datetime.strptime(data['fecha_sesion'], '%Y-%m-%d').date() if data.get('fecha_sesion') else None
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
            sesion.mejoras_observadas = data.get('mejoras_observadas', sesion.mejoras_observadas)
            sesion.feedback = data.get('feedback', sesion.feedback)
            sesion.notas = data.get('notas', sesion.notas)
            sesion.resultados_prueba = data.get('resultados_prueba', sesion.resultados_prueba)
            sesion.estado = data.get('estado', sesion.estado)
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
