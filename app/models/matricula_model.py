from datetime import datetime
from . import db
from .pago_model import Pago
from .persona_model import Persona
from .tipo_matricula_model import TipoMatricula

class Matricula(db.Model):
    __tablename__ = 'matricula'
    __table_args__ = {'schema': 'academico'}

    matrid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipmatrid = db.Column(db.Integer, db.ForeignKey('academico.tipo_matricula.tipmatrid'))
    matrfec = db.Column(db.Date)
    peridestudiante = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'))
    pagoidmatricula = db.Column(db.Integer, db.ForeignKey('academico.pago.pagid'))
    matrusureg = db.Column(db.String(50))
    matrfecreg = db.Column(db.DateTime)
    matrusumod = db.Column(db.String(50))
    matrfecmod = db.Column(db.DateTime)
    matrestado = db.Column(db.Integer)
    matrdescripcion = db.Column(db.String(255))

    pago = db.relationship('Pago', backref='matriculas', primaryjoin='Matricula.pagoidmatricula == Pago.pagid')
    estudiante = db.relationship('Persona', backref='matriculas', primaryjoin='Matricula.peridestudiante == Persona.perid')
    tipo_matricula = db.relationship('TipoMatricula', backref='matriculas', primaryjoin='Matricula.tipmatrid == TipoMatricula.tipmatrid')

    def __repr__(self):
        return f'<Matricula {self.matrid}>'

    def to_dict(self):
        return {
            'matrid': self.matrid,
            'tipmatrid': self.tipmatrid,
            'matrfec': self.matrfec.isoformat() if self.matrfec else None,
            'peridestudiante': self.peridestudiante,
            'pagoidmatricula': self.pagoidmatricula,
            'matrusureg': self.matrusureg,
            'matrfecreg': self.matrfecreg.isoformat() if self.matrfecreg else None,
            'matrusumod': self.matrusumod,
            'matrfecmod': self.matrfecmod.isoformat() if self.matrfecmod else None,
            'matrestado': self.matrestado,
            'matrdescripcion': self.matrdescripcion
        }
