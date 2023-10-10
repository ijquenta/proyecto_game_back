from client.responses import clientResponses
from core import configuration
from flask import request, abort
from http import HTTPStatus
import requests
reqUrl = "https://planillas.umsa.bo/auth_api/verify"




def checkBD(username, password):
    pass

def checkAuthorization(token, link):
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjA3NDY0ODYsIm5iZiI6MTY2MDc0NjQ4NiwianRpIjoiMDdlMWNlMGUtOTc1NS00MWUxLThkM2MtNDEwODI1OTkwYWE0IiwiZXhwIjoxNjYwODA2NDg2LCJpZGVudGl0eSI6ImE1OGYwODVjLTYwMjgtNDFmNi1hMjFiLTRiNGY3Zjc1NGZlZSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.6KPQn745tkSFgT5cIKa61BxQz8oVNNWgbvdDBHTaMd4" 
    }
    response = requests.get(url=reqUrl, headers=headersList)
    print(response.status_code)
    return True

def require_token():
    def intermediate(function):
        def wrapper(*args, **kwargs):
            if request.headers.get('token-authotization') and checkAuthorization(token=request.headers.get('token-authotization') ,link='link'):
                return function(*args, **kwargs)
            else:
                return clientResponses.accesoDenegado, HTTPStatus.UNAUTHORIZED
        return wrapper
    return intermediate



from jwt import encode, decode
from jwt import exceptions
from core import configuration
import os
from flask import jsonify

from datetime import datetime, timedelta

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

def write_token(data):
    token = encode(
        payload={**data, "exp": expire_date(1)},
        key=configuration.APP_SECRET_KEY,
        algorithm="HS256"
    )
    print("token->",token)
    return token.decode("utf-8")


def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=configuration.APP_SECRET_KEY, algorithm=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Expired Token"})
        response.status_code = 401
        return response