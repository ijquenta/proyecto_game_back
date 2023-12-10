from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

from core import configuration
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import logging

# Client
from client.responses import clientResponses as messages
from client.routes import Routes as routes

# Resources
import resources.Persona as Person
import resources.Reportes as Report
import resources.Usuario as Usuario
import resources.Materia as Materia
import resources.Curso as Curso
import resources.Nivel as Nivel
import resources.Autenticacion as Autenticacion
import services.nivel_service as NivelService
import resources.Inscripcion as Inscripcion
import resources.Matricula as Matricula
import resources.Rol as Rol
import resources.Estudiante as Estudiante
import resources.Docente as Docente
import resources.Nota as Nota
import resources.Pago as Pago
import resources.Asistencia as Asistencia
import resources.Material as Material

LOG_FILENAME = 'aplication.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=40000000, backupCount=40)
logger.addHandler(handler)

app = Flask(__name__)
app.config['SECRET_KEY'] = '67fcaee1a58b4bc7a0ff30c9d0036b5e'
jwt = JWTManager(app)
CORS(app)

@app.errorhandler(404)
def page_not_found(error):
    return messages._404, 404

@app.errorhandler(500)
def page_not_found(error):
    return messages._500, 500
    
api = Api(app)
app.secret_key = configuration.APP_SECRET_KEY

# api.add_resource(resources.Index, routes.index)
# api.add_resource(resources.Protected, routes.protected)

# API Usuarios
api.add_resource(Person.ListarUsuarios, routes.listaUsuarios)
api.add_resource(Usuario.GestionarUsuario, routes.gestionarUsuario)
api.add_resource(Usuario.ListaUsuario, routes.listaUsuario)
api.add_resource(Usuario.TipoPersona, routes.tipoPersona)
api.add_resource(Usuario.Perfil, routes.perfil)

# Reporte Prueba
api.add_resource(Report.rptTotalesSigma, routes.rptTotalesSigma)

# Roles
api.add_resource(Rol.ListarRoles, routes.listarRoles)
api.add_resource(Rol.GestionarRol, routes.gestionarRol)
# api.add_resource(Usuario.CrearRol, routes.crearRol)
# api.add_resource(Usuario.Login, routes.login)
# api.add_resource(Usuario.ModificarRol, routes.modificarRol)
# api.add_resource(Usuario.EliminarRol, routes.eliminarRol)

#Persona
api.add_resource(Usuario.ListarPersona, routes.listarPersona)
api.add_resource(Person.GestionarPersona, routes.gestionarPersona)
api.add_resource(Person.TipoDocumento, routes.tipoDocumento)
api.add_resource(Person.TipoEstadoCivil, routes.tipoEstadoCivil)
api.add_resource(Person.TipoGenero, routes.tipoGenero)
api.add_resource(Person.TipoPais, routes.tipoPais)
api.add_resource(Person.TipoCiudad, routes.tipoCiudad)
api.add_resource(Person.RegistrarPersona, routes.registrarPersona)

# Materia
api.add_resource(Materia.ListarMateria, routes.listarMateria)
api.add_resource(Materia.EliminarMateria, routes.eliminarMateria)
api.add_resource(Materia.InsertarMateria, routes.insertarMateria)
api.add_resource(Materia.ModificarMateria, routes.modificarMateria)

# Curso - Materia
api.add_resource(Curso.ListarCursoMateria, routes.listarCursoMateria)
api.add_resource(Curso.EliminarCursoMateria, routes.eliminarCursoMateria)
api.add_resource(Curso.InsertarCursoMateria, routes.insertarCursoMateria)
api.add_resource(Curso.ModificarCursoMateria, routes.modificarCursoMateria)
api.add_resource(Curso.TipoRol, routes.tipoRol)

# Combo
api.add_resource(Curso.ListaCursoCombo, routes.listaCursoCombo)
api.add_resource(Materia.ListaMateriaCombo, routes.listaMateriaCombo)
api.add_resource(Curso.ListaPersonaDocenteCombo, routes.listaPersonaDocenteCombo)

# Nivel
api.add_resource(Nivel.ListarNivel, routes.listarNivel)
api.add_resource(Nivel.InsertarNivel, routes.insertarNivel)
api.add_resource(Nivel.ModificarNivel, routes.modificarNivel)
api.add_resource(Nivel.EliminarNivel, routes.eliminarNivel)

# Inscripción
api.add_resource(Inscripcion.ListarInscripcion, routes.listarInscripcion)
api.add_resource(Inscripcion.InsertarInscripcion, routes.insertarInscripcion)
api.add_resource(Inscripcion.ModificarInscripcion, routes.modificarInscripcion)
api.add_resource(Inscripcion.EliminarInscripcion, routes.eliminarInscripcion)
api.add_resource(Inscripcion.ObtenerCursoMateria, routes.obtenerCursoMateria)
api.add_resource(Inscripcion.ListarComboCursoMateria, routes.listarComboCursoMateria)
api.add_resource(Inscripcion.ListarComboMatricula, routes.listarComboMatricula)

# Matricula
api.add_resource(Matricula.ListarMatricula, routes.listarMatricula)
api.add_resource(Matricula.InsertarMatricula, routes.insertarMatricula)
api.add_resource(Matricula.ModificarMatricula, routes.modificarMatricula)
api.add_resource(Matricula.EliminarMatricula, routes.eliminarMatricula)

# Estudiante
api.add_resource(Estudiante.ListarEstudiante, routes.listarEstudiante)
api.add_resource(Estudiante.ObtenerMateriasInscritas, routes.obtenerMateriasInscritas)

# Docente
api.add_resource(Docente.ListarDocente, routes.listarDocente)
api.add_resource(Docente.ObtenerMateriasAsignadas, routes.obtenerMateriasAsignadas)

# Nota
api.add_resource(Nota.ListarNota, routes.listarNota)
api.add_resource(Nota.GestionarNota, routes.gestionarNota)
api.add_resource(Nota.ListarNotaEstudiante, routes.listarNotaEstudiante)
api.add_resource(Nota.ListarNotaDocente, routes.listarNotaDocente)
api.add_resource(Nota.ListarNotaEstudianteMateria, routes.listarNotaEstudianteMateria)
api.add_resource(Nota.ListarNotaEstudianteCurso, routes.listarNotaEstudianteCurso)
api.add_resource(Nota.RptNotaEstudianteMateria, routes.rptNotaEstudianteMateria)


# Pago
api.add_resource(Pago.ListarPago, routes.listarPago)

# Asistencia
api.add_resource(Asistencia.ListarAsistencia, routes.listarAsistencia)

# Material
api.add_resource(Material.ListarMaterial, routes.listarMaterial)


import jwt
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123456@localhost/db_academico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Persona(db.Model):
    __tablename__ = 'persona'
    __table_args__ = {'schema': 'academico'}
    perid = db.Column(db.Integer, primary_key=True)
    pernomcompleto = db.Column(db.String)
    pernombres = db.Column(db.String(100), nullable=False)
    perapepat = db.Column(db.String(100))
    perapemat = db.Column(db.String(100))
    pertipodoc = db.Column(db.Integer)
    pernrodoc = db.Column(db.Integer)
    perfecnac = db.Column(db.Date)
    perdirec = db.Column(db.Text)
    peremail = db.Column(db.String(100))
    percelular = db.Column(db.String(20))
    pertelefono = db.Column(db.String(20))
    perpais = db.Column(db.Integer)
    perciudad = db.Column(db.Integer)
    pergenero = db.Column(db.Integer)
    perestcivil = db.Column(db.Integer)
    perfoto = db.Column(db.String)
    perestado = db.Column(db.SmallInteger, default=1)
    perobservacion = db.Column(db.String(255))
    perusureg = db.Column(db.String(50))
    perfecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    perusumod = db.Column(db.String(50))
    perfecmod = db.Column(db.TIMESTAMP)

class Rol(db.Model):
    __tablename__ = 'rol'
    __table_args__ = {'schema': 'academico'}
    rolid = db.Column(db.Integer, primary_key=True)
    rolnombre = db.Column(db.String(50), nullable=False)
    roldescripcion = db.Column(db.String(255))
    rolusureg = db.Column(db.String(50))
    rolfecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    rolusumod = db.Column(db.String(50))
    rolfecmod = db.Column(db.TIMESTAMP)
    rolestado = db.Column(db.SmallInteger, default=1)
     
class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'academico'}
    usuid = db.Column(db.Integer, primary_key=True)
    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'))
    rolid = db.Column(db.Integer, db.ForeignKey('academico.rol.rolid'))
    usuname = db.Column(db.String(50), nullable=False)
    usupassword = db.Column(db.String(100), nullable=False)
    usupasswordhash = db.Column(db.String, nullable=False)
    usuemail = db.Column(db.String(100), nullable=False)
    usuimagen = db.Column(db.String(255))
    usudescripcion = db.Column(db.String(255))
    usuestado = db.Column(db.SmallInteger, default=1)
    usuusureg = db.Column(db.String(50))
    usufecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    usuusumod = db.Column(db.String(50))
    usufecmod = db.Column(db.TIMESTAMP)
    
    persona = db.relationship('Persona', backref=db.backref('usuarios', lazy=True))
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
    
def encode_token(user_id, user_rol):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1,minutes=0,seconds=0),
        'iat': datetime.utcnow(),
        'sub': user_id,
        'rol': user_rol 
    }
    token = jwt.encode(payload, configuration.APP_SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')

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
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
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

@app.route('/academico_api/register', methods=['POST'])
def register_user():
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
            # print(e)
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
        
@app.route('/academico_api/login', methods = ['POST'])
def post():
    user_data = request.get_json()
    try:
        user = Usuario.query.filter_by(usuname = user_data['usuname']).first()
        if user and check_password_hash(user.usupassword, user_data['usupassword']) == True:
            rol = Rol.query.get(user.rolid)
            auth_token = encode_token(user.usuid, rol.rolnombre)
            resp = {
                "status":"succes",
                "message" :"Successfully logged in",
                'auth_token':auth_token,
                "usuario": user.usuid,
                "rol": rol.rolnombre,
            }
            return make_response(jsonify(resp)),200
        else:
            resp ={
                "status":"Error",
                "message":"User does not exist"
            }
            return make_response(jsonify(resp)), 404
    except Exception as e:
        print(e)
        resp = {
            "Status":"error",
            "Message":"User login failed"
        }
        return make_response(jsonify(resp)), 404

@app.route('/protected', methods=['GET'])
@token_required 
def protected():
   resp = {"message": "Tienes acceso a esta API"}
   return make_response(jsonify(resp)), 200


if __name__ == '__main__':
	HOST = configuration.SERVER_HOST
	PORT = configuration.SERVER_PORT
	DEBUG = configuration.DEBUG
	print (HOST,PORT, ':3')
	app.run(host=HOST,port=PORT,debug=True)