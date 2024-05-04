from . import db
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuario
from models.rol import Rol
from resources.Autenticacion import TokenGenerator

def f_register_usuario():
    user_data = request.get_json()
    user = Usuario.query.filter_by(usuname = user_data['usuname']).first()
    if not user:
        try: 
            hashed_password = generate_password_hash(user_data['usupassword'])
            user_new = Usuario(usuname = user_data['usuname'], usupassword = hashed_password, perid = user_data['perid'], rolid = user_data['rolid'])
            db.session.add(user_new)
            db.session.commit()
            resp = {
                "status":"success",
                "message":"User successfully registered",
            }
            return make_response(jsonify(resp)),201
        except Exception as e:
            print(e)
            resp = {
                "status" :"Error",
                "message" :" Error occured, user registration failed"
            }
            return make_response(jsonify(resp)),401
    else:
        resp = {
            "status":"error",
            "message":"User already exists"
        }
        return make_response(jsonify(resp)),202


def f_login_usuario():
    user_data = request.get_json()

    if 'usuname' not in user_data or 'usupassword' not in user_data: # Verificar si los campos requeridos están presentes en la solicitud
        return jsonify({"status": "Error", "message": "Missing username or password"}), 400

    try: # recuperar el usuario de la base de datos
        user = Usuario.query.filter_by(usuname=user_data['usuname']).first()
        
        if user and check_password_hash(user.usupassword, user_data['usupassword']): # Verificar si el usuario existe y la contraseña es correcta
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
    
    except Exception as e: # Capturar cualquier excepción que pueda ocurrir durante la ejecución
        print("Error f_login_usuario: ",e)
        return jsonify({"status": "Error", "message": "Internal server error"}), 500