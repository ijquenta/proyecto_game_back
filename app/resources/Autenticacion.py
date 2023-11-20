# from flask_restful import Resource, reqparse
# from flask_jwt_extended import JWTManager
# from core import configuration
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify, make_response
# from werkzeug.security import generate_password_hash, check_password_hash
# from functools import wraps
# import jwt
# from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__) 
# # Configuración de la base de datos
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key = True, autoincrement= True)
#     email = db.Column(db.String(150), unique = True, nullable = False)
#     password = db.Column(db.String(150), nullable = False)
#     date_registered = db.Column(db.DateTime, default = datetime.utcnow())

#     @classmethod
#     def get_by_id(cls, user_id):
#         return cls.query.get(user_id)

# def encode_token(user_id, user_email):
#     print("encode_token: Datos recibidos: ", user_id, user_email)
#     payload = {
#         'exp': datetime.utcnow() + timedelta(days=0,seconds=30),
#         'iat': datetime.utcnow(),
#         'sub': user_id,
#         'email': user_email 
#     }
#     print("Payload: ", payload)
#     token = jwt.encode(payload, configuration.APP_SECRET_KEY, algorithm='HS256')
#     print("Token Generado: ", token.decode('utf-8'))
#     return token.decode('utf-8')


# from flask import Flask,request,jsonify,make_response
# from werkzeug.security import generate_password_hash

# class UserLogin(Resource):
#     def post(self):
#         user_data = request.get_json()

#         user = User.query.filter_by(email=user_data['email']).first()
#         if user and check_password_hash(user.password, user_data['password'])==True:
#             auth_token = encode_token(user.id, user.email)

#             resp = {
#                 "status":"Succes",
#                 "message" :"Successfully logged in",
#                 'auth_token':auth_token,
#                 "usuario": user.id,
#                 "email": user.email,
#             }
#             return jsonify(resp),200
#         else:
#             resp ={
#                 "status":"Error",
#                 "message":"User does not exist"
#             }
#             return jsonify(resp), 404

# class RegisterUser(Resource):
#     def post(self):
#         user_data = request.get_json()

#         user = User.query.filter_by(email=user_data['email']).first()
#         if not user:
#             try:
#                 hashed_password = generate_password_hash(user_data['password'])
#                 user_new = User(email=user_data['email'], password=hashed_password)
#                 db.session.add(user_new)
#                 db.session.commit()

#                 resp = {
#                     "status":"success",
#                     "message":"User successfully registered",
#                 }
#                 return jsonify(resp),201

#             except Exception as e:
#                 resp = {
#                     "status" :"Error",
#                     "message" :" Error occured, user registration failed"
#                 }
#                 return jsonify(resp),401
#         else:
#             resp = {
#                 "status":"error",
#                 "message":"User already exists"
#             }
#             return jsonify(resp),202