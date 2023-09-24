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