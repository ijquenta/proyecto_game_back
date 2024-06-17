from datetime import datetime
from . import db


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
