from flask import jsonify
from core.database import db, as_string, select, execute, execute_function, execute_response, sql
from utils.date_formatting import *
from models.rol import Rol
from models.permiso import Permiso
from models.operacion import Operacion


def getTipoOperacion():
    return select(f''' SELECT opeid, openombre FROM academico.operacion order by openombre;''')

