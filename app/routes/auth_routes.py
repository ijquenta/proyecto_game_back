from . import db
from flask import request, jsonify
from werkzeug.security import check_password_hash
from models.usuario_model import Usuario
from models.rol_model import Rol
from resources.Autenticacion import TokenGenerator


import bcrypt
def f_login_usuario(bcrypt):
    user_data = request.get_json()
    # Verificar si los campos requeridos están presentes en la solicitud
    if 'usuname' not in user_data or 'usupassword' not in user_data:
        return jsonify({"status": "Error", "message": "Missing username or password"}), 400

    try:  # recuperar el usuario de la base de datos
        user = Usuario.query.filter_by(usuname=user_data['usuname']).first()

        if user:
            if not user.usuconfirmado:  # Verificar si el usuario está confirmado por correo electrónico
                return jsonify({"status": "Error", "message": "Email not confirmed. Please confirm your email before logging in."}), 401

            # Verificar si la contraseña es correcta
            if bcrypt.check_password_hash(user.usupassword, user_data['usupassword']):
                rol = Rol.query.get(user.rolid)
                auth_token = TokenGenerator.encode_token(
                    user.usuid, rol.rolnombre)
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

    except Exception as e:
        print("Error login user: ", e)
        db.session.rollback()  # Deshacer los cambios si ocurre alguna falla
        return jsonify({
            "status": "Error",
            "message": "Internal server error",
            "error": str(e)
        }), 500
