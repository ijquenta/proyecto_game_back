from . import db
# from . import mail  # Importa mail desde app.py
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuario
from models.rol import Rol
from resources.Autenticacion import TokenGenerator
from flask_mail import Mail, Message  # Para el servicio de correo electrónico
import os

def f_register_usuario():
    user_data = request.get_json()
    print("1. datos enviados: ", user_data)
    user = Usuario.query.filter_by(usuname=user_data['usuname']).first()
    if not user:
        try: 
            hashed_password = generate_password_hash(user_data['usupassword'])

            user_new = Usuario(
                usuname=user_data['usuname'],
                usupassword=hashed_password,
                usupasswordhash=hashed_password,
                perid=user_data['perid'],
                rolid=user_data['rolid'],
                usuemail=user_data['usuemail'],
                usudescripcion=user_data['usudescripcion'],
                usuusureg=user_data['usuusureg'],
                usuestado=user_data['usuestado']
            )
            
            print("2. usuario nuevo:", user_new)
            
            db.session.add(user_new)
            db.session.commit()

            # Genera el token de confirmación
            confirmation_token = TokenGenerator.generate_confirmation_token(user_new.usuid, user_new.rolid)
            
            print("3. se genera el token: ", confirmation_token)

            # Prepara el mensaje de correo electrónico de confirmación
            mensaje_correo = f'Por favor, haga clic en el siguiente enlace para confirmar su registro: http://127.0.0.0:4200/confirm-email?token={confirmation_token}'

            print("4. se agrega el mensaje: ", mensaje_correo)

            # Envía el correo electrónico de confirmación
            if enviar_correo(user_data['usuemail'], 'Confirmación de registro', mensaje_correo):
                resp = {
                    "status": "success",
                    "message": "User successfully registered. Confirmation email sent."
                }
                return make_response(jsonify(resp)), 201
            else:
                resp = {
                    "status": "Error",
                    "message": "Error occurred while sending confirmation email"
                }
                return make_response(jsonify(resp)), 500

        except Exception as e:
            print(e)
            resp = {
                "status": "Error",
                "message": "Error occurred, user registration failed"
            }
            return make_response(jsonify(resp)), 401
    else:
        resp = {
            "status": "error",
            "message": "User already exists"
        }
        return make_response(jsonify(resp)), 202


def f_login_usuario():
    user_data = request.get_json()

    if 'usuname' not in user_data or 'usupassword' not in user_data: # Verificar si los campos requeridos están presentes en la solicitud
        return jsonify({"status": "Error", "message": "Missing username or password"}), 400

    try: # recuperar el usuario de la base de datos
        user = Usuario.query.filter_by(usuname=user_data['usuname']).first()
        
        if user:
            if not user.usuconfirmado:  # Verificar si el usuario está confirmado por correo electrónico
                return jsonify({"status": "Error", "message": "Email not confirmed. Please confirm your email before logging in."}), 401
            
            if check_password_hash(user.usupassword, user_data['usupassword']): # Verificar si la contraseña es correcta
                rol = Rol.query.get(user.rolid)
                auth_token = TokenGenerator.encode_token(user.usuid, rol.rolnombre)
                resp = {
                    "status": "success",
                    "message": "Successfully logged in",
                    'auth_token': auth_token,
                    "usuario": user.usuid,
                    "rol": rol.rolnombre,
                }
                return jsonify(resp), 200
            else:
                return jsonify({"status": "Error", "message": "Invalid username or password"}), 401
        else:
            return jsonify({"status": "Error", "message": "Invalid username or password"}), 401
    
    except Exception as e: # Capturar cualquier excepción que pueda ocurrir durante la ejecución
        print("Error f_login_usuario: ",e)
        return jsonify({"status": "Error", "message": "Internal server error"}), 500


# def enviar_correo(destinatario, asunto, mensaje):
#     print("esta es la variable de entorno de email: ",os.environ.get("EMAIL_HOST_USER") )
#     try:
#         msg = Message(sender=os.environ.get("EMAIL_HOST_USER"),
#                       subject=asunto,
#                       recipients=[destinatario],
#                       body=mensaje)
#         mail.send(msg)
#         return True
#     except Exception as e:
#         print(f'Error al enviar el correo: {str(e)}')
#         return False
