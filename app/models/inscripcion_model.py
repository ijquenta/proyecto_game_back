from datetime import datetime
from . import db
from .curso_materia_model import CursoMateria
from .matricula_model import Matricula
from .pago_model import Pago
from .persona_model import Persona

class Inscripcion(db.Model):
    __tablename__ = 'inscripcion'
    __table_args__ = {'schema': 'academico'}

    insid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matrid = db.Column(db.Integer, db.ForeignKey('academico.matricula.matrid'))
    peridestudiante = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'))
    pagid = db.Column(db.Integer, db.ForeignKey('academico.pago.pagid'))
    insusureg = db.Column(db.String(50))
    insfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    insusumod = db.Column(db.String(50))
    insfecmod = db.Column(db.DateTime)
    curmatid = db.Column(db.Integer, db.ForeignKey('academico.curso_materia.curmatid'))
    insestado = db.Column(db.SmallInteger, default=0, nullable=False)
    insestadodescripcion = db.Column(db.String)

    curso_materia = db.relationship('CursoMateria', backref='inscripciones', primaryjoin='Inscripcion.curmatid == CursoMateria.curmatid')
    matricula = db.relationship('Matricula', backref='inscripciones', primaryjoin='Inscripcion.matrid == Matricula.matrid')
    pago = db.relationship('Pago', backref='inscripciones', primaryjoin='Inscripcion.pagid == Pago.pagid')
    estudiante = db.relationship('Persona', backref='inscripciones', primaryjoin='Inscripcion.peridestudiante == Persona.perid')

    def __repr__(self):
        return f'<Inscripcion {self.insid}>'

    def to_dict(self):
        return {
            'insid': self.insid,
            'matrid': self.matrid,
            'peridestudiante': self.peridestudiante,
            'pagid': self.pagid,
            'insusureg': self.insusureg,
            'insfecreg': self.insfecreg.isoformat() if self.insfecreg else None,
            'insusumod': self.insusumod,
            'insfecmod': self.insfecmod.isoformat() if self.insfecmod else None,
            'curmatid': self.curmatid,
            'insestado': self.insestado,
            'insestadodescripcion': self.insestadodescripcion
        }
