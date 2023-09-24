from . import configuration
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate
from core import configuration
from psycopg2 import sql
from datetime import datetime
from re import sub
import pandas as pd
import json
from http import HTTPStatus
from client.responses import clientResponses as messages

import psycopg2.extensions

engine = create_engine(configuration.SQLALCHEMY_DATABASE_URL,pool_size=40,
                                      max_overflow=8,
                                      pool_recycle=600,
                                      pool_pre_ping=True,
                                      pool_use_lifo=True)
Base = declarative_base()
Session = sessionmaker(engine)
session_db = Session()
db = SQLAlchemy()


def as_string(composable, encoding="utf-8"):
    if isinstance(composable, sql.Composed):
        return ''.join([as_string(x, encoding) for x in composable])
    elif isinstance(composable, sql.SQL):
        return composable.string
    else:
        rv = sql.ext.adapt(composable._wrapped)
        if isinstance(rv, psycopg2.extensions.QuotedString): rv.encoding = encoding
        rv = rv.getquoted()
        return rv.decode(encoding) if isinstance(rv, bytes) else rv

def camel_case(s):   
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])

def renameCols(cols):
    newCols = []
    for col in cols:
        newCols.append(camel_case(col))
    return newCols

def select(query):
    df = pd.read_sql_query(query, engine)
    df.columns = renameCols(df.columns)
    jsonData = df.to_json(orient='records', date_format='iso')
    return json.loads(jsonData)


def execute(query):
    try:
        session_db.execute(query)
        session_db.commit()
        return messages.success, HTTPStatus.OK
    except Exception as err:
        session_db.rollback()
        print(err)
        return {"code": 0, "message": f"Error: {err}"}, HTTPStatus.NOT_FOUND
