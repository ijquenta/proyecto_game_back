# Librerías de Flask y Werkzeug
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Librerías de PostgreSQL y SQLAlchemy
from psycopg2 import sql
from sqlalchemy import or_

# Modelos de la aplicación
from models.persona_model import Persona
from models.rol import Rol

# Recursos y servicios
from resources.Autenticacion import TokenGenerator
from services.email_service import EmailService

# Utilidades y funciones auxiliares
from utils.date_formatting import *
from core.database import select, execute, as_string
# from app.utils.email import send_reset_email  # Comentado temporalmente

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
        users = db.session.query(Usuario).all()
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
from models.usuario import Usuario, db
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