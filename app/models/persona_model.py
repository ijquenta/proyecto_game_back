from datetime import datetime
from . import db
from models.tipo_ciudad_model import TipoCiudad
from models.tipo_documento_model import TipoDocumento
from models.tipo_estado_civil_model import TipoEstadoCivil
from models.tipo_genero_model import TipoGenero
from models.tipo_pais_model import TipoPais

class Persona(db.Model):
    __tablename__ = 'persona'
    __table_args__ = {'schema': 'academico'}

    perid = db.Column(db.Integer, primary_key=True)
    pernomcompleto = db.Column(db.String)
    pernombres = db.Column(db.String(100), nullable=False)
    perapepat = db.Column(db.String(100))
    perapemat = db.Column(db.String(100))
    pertipodoc = db.Column(db.Integer, db.ForeignKey('academico.tipo_documento.tipodocid'))
    pernrodoc = db.Column(db.String)
    perfecnac = db.Column(db.Date)
    perdirec = db.Column(db.Text)
    peremail = db.Column(db.String(100))
    percelular = db.Column(db.String(20))
    pertelefono = db.Column(db.String(20))
    perpais = db.Column(db.Integer, db.ForeignKey('academico.tipo_pais.paisid'))
    perciudad = db.Column(db.Integer, db.ForeignKey('academico.tipo_ciudad.ciudadid'))
    pergenero = db.Column(db.Integer, db.ForeignKey('academico.tipo_genero.generoid'))
    perestcivil = db.Column(db.Integer, db.ForeignKey('academico.tipo_estadocivil.estadocivilid'))
    perfoto = db.Column(db.String)
    perestado = db.Column(db.SmallInteger, default=1)
    perobservacion = db.Column(db.String(255))
    perusureg = db.Column(db.String(50))
    perfecreg = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    perusumod = db.Column(db.String(50))
    perfecmod = db.Column(db.TIMESTAMP)

    # Relaciones
    tipo_documento = db.relationship('TipoDocumento', foreign_keys=[pertipodoc])
    tipo_pais = db.relationship('TipoPais', foreign_keys=[perpais])
    tipo_ciudad = db.relationship('TipoCiudad', foreign_keys=[perciudad])
    tipo_genero = db.relationship('TipoGenero', foreign_keys=[pergenero])
    tipo_estadocivil = db.relationship('TipoEstadoCivil', foreign_keys=[perestcivil])

    def to_dict(self):
        return {
            'perid': self.perid,
            'pernomcompleto': self.pernomcompleto,
            'pernombres': self.pernombres,
            'perapepat': self.perapepat,
            'perapemat': self.perapemat,
            'pertipodoc': self.pertipodoc,
            'tipodocnombre': self.tipo_documento.tipodocnombre if self.tipo_documento else None,
            'pernrodoc': self.pernrodoc,
            'perfecnac': self.perfecnac.isoformat() if self.perfecnac else None,
            'perdirec': self.perdirec,
            'peremail': self.peremail,
            'percelular': self.percelular,
            'pertelefono': self.pertelefono,
            'perpais': self.perpais,
            'paisnombre': self.tipo_pais.paisnombre if self.tipo_pais else None,
            'perciudad': self.perciudad,
            'ciudadnombre': self.tipo_ciudad.ciudadnombre if self.tipo_ciudad else None,
            'pergenero': self.pergenero,
            'generonombre': self.tipo_genero.generonombre if self.tipo_genero else None,
            'perestcivil': self.perestcivil,
            'estadocivilnombre': self.tipo_estadocivil.estadocivilnombre if self.tipo_estadocivil else None,
            'perfoto': self.perfoto,
            'perestado': self.perestado,
            'perobservacion': self.perobservacion,
            'perusureg': self.perusureg,
            'perfecreg': self.perfecreg.isoformat() if self.perfecreg else None,
            'perusumod': self.perusumod,
            'perfecmod': self.perfecmod.isoformat() if self.perfecmod else None
        }


class PersonaInfoPersonal(db.Model):
    __tablename__ = 'persona_info_personal'
    __table_args__ = {'schema': 'academico'}

    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'), nullable=False, primary_key=True)
    peredad = db.Column(db.Integer, nullable=True)
    pernrohijos = db.Column(db.Integer, nullable=True)
    perprofesion = db.Column(db.Integer, nullable=True)
    perfecconversion = db.Column(db.Date, nullable=True)
    perlugconversion = db.Column(db.String(255), nullable=True)
    perbautizoagua = db.Column(db.SmallInteger, nullable=True)
    perbautizoespiritu = db.Column(db.SmallInteger, nullable=True)
    pernomiglesia = db.Column(db.String(255), nullable=True)
    perdiriglesia = db.Column(db.String(255), nullable=True)
    pernompastor = db.Column(db.String(50), nullable=True)
    percelpastor = db.Column(db.Integer, nullable=True)
    perusureg = db.Column(db.String(50), nullable=True)
    perfecreg = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    perusumod = db.Column(db.String(50), nullable=True)
    perfecmod = db.Column(db.TIMESTAMP, nullable=True)
    perobservacion = db.Column(db.String(255), nullable=True)
    perestado = db.Column(db.SmallInteger, nullable=True)
    perexperiencia = db.Column(db.Integer, nullable=True)
    permotivo = db.Column(db.String(255), nullable=True)
    perplanesmetas = db.Column(db.String(255), nullable=True)

    # Relación con la tabla Persona
    persona = db.relationship('Persona', backref='info_personal')

    def to_dict(self):
        return {
            'perid': self.perid,
            'peredad': self.peredad,
            'pernrohijos': self.pernrohijos,
            'perprofesion': self.perprofesion,
            'perfecconversion': self.perfecconversion.isoformat() if self.perfecconversion else None,
            'perlugconversion': self.perlugconversion,
            'perbautizoagua': self.perbautizoagua,
            'perbautizoespiritu': self.perbautizoespiritu,
            'pernomiglesia': self.pernomiglesia,
            'perdiriglesia': self.perdiriglesia,
            'pernompastor': self.pernompastor,
            'percelpastor': self.percelpastor,
            'perexperiencia': self.perexperiencia,
            'permotivo': self.permotivo,
            'perplanesmetas': self.perplanesmetas,                                                      
            'perusureg': self.perusureg,
            'perfecreg': self.perfecreg.isoformat() if self.perfecreg else None,
            'perusumod': self.perusumod,
            'perfecmod': self.perfecmod.isoformat() if self.perfecmod else None,
            'perobservacion': self.perobservacion,
            'perestado': self.perestado
        }
        

class PersonaInfoMinisterial(db.Model):
    __tablename__ = 'persona_info_ministerial'
    __table_args__ = {'schema': 'academico'}

    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'), nullable=False, primary_key=True)
    pernomiglesia = db.Column(db.String(100), nullable=True)
    percargo = db.Column(db.Integer, nullable=True)
    pergestion = db.Column(db.Integer, nullable=True)
    perusureg = db.Column(db.String(50), nullable=True)
    perfecreg = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    perusumod = db.Column(db.String(50), nullable=True)
    perfecmod = db.Column(db.TIMESTAMP, nullable=True)
    perobservacion = db.Column(db.String(255), nullable=True)
    perestado = db.Column(db.SmallInteger, nullable=True)
    perinfomin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    

    def to_dict(self):
        return {
            'perinfomin': self.perinfomin,
            'perid': self.perid,
            'pernomiglesia': self.pernomiglesia,
            'percargo': self.percargo,
            'pergestion': self.pergestion,             
            'perusureg': self.perusureg,
            'perfecreg': self.perfecreg.isoformat() if self.perfecreg else None,
            'perusumod': self.perusumod,
            'perfecmod': self.perfecmod.isoformat() if self.perfecmod else None,
            'perobservacion': self.perobservacion,
            'perestado': self.perestado
        }


class PersonaInfoAcademica(db.Model):
    __tablename__ = 'persona_info_academica'
    __table_args__ = {'schema': 'academico'}

    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'), nullable=False, primary_key=True)
    pereducacion = db.Column(db.Integer, nullable=True)
    pernominstitucion = db.Column(db.String(100), nullable=True)
    perdirinstitucion = db.Column(db.String(150), nullable=True)
    pergescursadas = db.Column(db.String(50), nullable=True)
    perfechas = db.Column(db.String(150), nullable=True)
    pertitulo = db.Column(db.String(100), nullable=True)
    perusureg = db.Column(db.String(50), nullable=True)
    perfecreg = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    perusumod = db.Column(db.String(50), nullable=True)
    perfecmod = db.Column(db.TIMESTAMP, nullable=True)
    perobservacion = db.Column(db.String(255), nullable=True)
    perestado = db.Column(db.SmallInteger, nullable=True)
    perinfoaca = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        return {
            'perinfoaca': self.perinfoaca,
            'perid': self.perid,
            'pereducacion': self.pereducacion,
            'pernominstitucion': self.pernominstitucion,
            'perdirinstitucion': self.perdirinstitucion,
            'pergescursadas': self.pergescursadas,
            'perfechas': self.perfechas,
            'pertitulo': self.pertitulo,
            'perusureg': self.perusureg,
            'perfecreg': self.perfecreg.isoformat() if self.perfecreg else None,
            'perusumod': self.perusumod,
            'perfecmod': self.perfecmod.isoformat() if self.perfecmod else None,
            'perobservacion': self.perobservacion,
            'perestado': self.perestado
        }
        

class PersonaDocAdmision(db.Model):
    __tablename__ = 'persona_doc_admision'
    __table_args__ = {'schema': 'academico'}

    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'), nullable=False, primary_key=True)
    perfoto = db.Column(db.String(255), nullable=True)
    perfotoci = db.Column(db.String(255), nullable=True)
    perfototitulo = db.Column(db.String(255), nullable=True)
    percartapastor = db.Column(db.String(255), nullable=True)
    perusureg = db.Column(db.String(50), nullable=True)
    perfecreg = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    perusumod = db.Column(db.String(50), nullable=True)
    perfecmod = db.Column(db.TIMESTAMP, nullable=True)
    perobservacion = db.Column(db.String(255), nullable=True)
    perestado = db.Column(db.SmallInteger, nullable=True)
 
    def to_dict(self):
        return {
            'perid': self.perid,
            'perfoto': self.perfoto,
            'perfotoci': self.perfotoci,
            'perfototitulo': self.perfototitulo,
            'percartapastor': self.percartapastor,
            'perusureg': self.perusureg,
            'perfecreg': self.perfecreg.isoformat() if self.perfecreg else None,
            'perusumod': self.perusumod,
            'perfecmod': self.perfecmod.isoformat() if self.perfecmod else None,
            'perobservacion': self.perobservacion,
            'perestado': self.perestado
        }
        
        
class TipoProfesion(db.Model):
    __tablename__ = 'tipo_profesion'
    __table_args__ = {'schema': 'academico'}

    proid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pronombre = db.Column(db.String(100))
    prousureg = db.Column(db.String(50))
    profecreg = db.Column(db.DateTime, default=datetime.utcnow)
    prousumod = db.Column(db.String(50))
    profecmod = db.Column(db.DateTime, onupdate=datetime.utcnow)
    proobservacion = db.Column(db.String(255))
    proestado = db.Column(db.SmallInteger)

    def __init__(self, 
                pronombre=None, 
                prousureg=None, 
                profecreg=None, 
                profecmod=None,
                prousumod=None, 
                proobservacion=None, 
                proestado=None
                ):
        self.pronombre = pronombre
        self.prousureg = prousureg
        self.profecreg = profecreg
        self.prousumod = prousumod
        self.profecmod = profecmod
        self.proobservacion = proobservacion
        self.proestado = proestado

    def __repr__(self):
        return f'<TipoProfesion {self.pronombre}>'
    
    def to_dict(self):
        return {
            'proid': self.proid,
            'pronombre': self.pronombre,
            'prousureg': self.prousureg,
            'profecreg': self.profecreg.isoformat() if self.profecreg else None,
            'prousumod': self.prousumod,
            'profecmod': self.profecmod.isoformat() if self.profecmod else None,
            'proobservacion': self.proobservacion,
            'proestado': self.proestado
        }


class TipoEducacion(db.Model):
    __tablename__ = 'tipo_educacion'
    __table_args__ = {'schema': 'academico'}

    eduid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edunombre = db.Column(db.String(100))
    eduusureg = db.Column(db.String(50))
    edufecreg = db.Column(db.DateTime, default=datetime.utcnow)
    eduusumod = db.Column(db.String(50))
    edufecmod = db.Column(db.DateTime, onupdate=datetime.utcnow)
    eduobservacion = db.Column(db.String(255))
    eduestado = db.Column(db.SmallInteger)

    def __init__(self, 
                edunombre=None, 
                eduusureg=None, 
                edufecreg=None, 
                eduusumod=None, 
                edufecmod=None, 
                eduobservacion=None, 
                eduestado=None
                ):
        self.edunombre = edunombre
        self.eduusureg = eduusureg
        self.edufecreg = edufecreg
        self.eduusumod = eduusumod
        self.edufecmod = edufecmod
        self.eduobservacion = eduobservacion
        self.eduestado = eduestado

    def __repr__(self):
        return f'<TipoEducacion {self.edunombre}>'
    
    def to_dict(self):
        return {
            'eduid': self.eduid,
            'edunombre': self.edunombre,
            'eduusureg': self.eduusureg,
            'edufecreg': self.edufecreg.isoformat() if self.edufecreg else None,
            'eduusumod': self.eduusumod,
            'edufecmod': self.edufecmod.isoformat() if self.edufecmod else None,
            'eduobservacion': self.eduobservacion,
            'eduestado': self.eduestado
        }


class TipoCargo(db.Model):
    __tablename__ = 'tipo_cargo'
    __table_args__ = {'schema': 'academico'}

    carid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    carnombre = db.Column(db.String(100))
    carusureg = db.Column(db.String(50))
    carfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    carusumod = db.Column(db.String(50))
    carfecmod = db.Column(db.DateTime, onupdate=datetime.utcnow)
    carobservacion = db.Column(db.String(255))
    carestado = db.Column(db.SmallInteger)

    def __init__(self,
                carnombre=None,
                carusureg=None,
                carfecreg=None,
                carusumod=None,
                carfecmod=None,
                carobservacion=None,
                carestado=None
                ):
        self.carnombre = carnombre
        self.carusureg = carusureg
        self.carfecreg = carfecreg
        self.carusumod = carusumod
        self.carfecmod = carfecmod
        self.carobservacion = carobservacion
        self.carestado = carestado
    
    def __repr__(self):
        return f'<TipoCargo {self.carnombre}>'
    
    def to_dict(self):
        return {
            'carid': self.carid,
            'carnombre': self.carnombre,
            'carusureg': self.carusureg,
            'carfecreg': self.carfecreg.isoformat() if self.carfecreg else None,
            'carusumod': self.carusumod,
            'carfecmod': self.carfecmod.isoformat() if self.carfecmod else None,
            'carobservacion': self.carobservacion,
            'carestado': self.carestado
        }