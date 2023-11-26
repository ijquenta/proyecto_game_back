from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from core import configuration


app = Flask(__name__) # Aplicación Flask
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'
jwt = JWTManager(app)

from flask import Flask,request,jsonify,make_response
from werkzeug.security import generate_password_hash
# from resources.Autenticacion import User, db,check_password_hash, encode_token, token_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

CORS(app)

    
api = Api(app)

app.secret_key = configuration.APP_SECRET_KEY

# class Rol(db.Model):
#     __tablename__ = 'rol'
#     __table_args__ = {'schema': 'academico'}
#     rolid = db.Column(db.Integer, primary_key=True)
#     rolnombre = db.Column(db.String(50), nullable=False)
#     roldescripcion = db.Column(db.String(255))
#     rolusureg = db.Column(db.String(50))
#     rolfecreg = db.Column(db.TIMESTAMP, default=db.func.now())
#     rolusumod = db.Column(db.String(50))
#     rolfecmod = db.Column(db.TIMESTAMP)
#     rolestado = db.Column(db.SmallInteger, default=1)
