import jwt
from functools import wraps
from flask import request
import os
from models.usuario import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing",
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, os.environ.get("APP_SECRET_KEY"), algorithms=["HS256"])
            # data=TokenGenerator.decode_token(token)
            current_user=Usuario().get_by_id(data["sub"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token",
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "An error Occured",
                "error": str(e)
            }, 401
        return f(*args, **kwargs)
    return decorated
