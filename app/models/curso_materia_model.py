from datetime import datetime
from . import db
from .curso_model import Curso
from .materia_model import Materia
from .persona_model import Persona

class CursoMateria(db.Model):
    __tablename__ = 'curso_materia'
    __table_args__ = {'schema': 'academico'}

    curmatid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curid = db.Column(db.Integer, db.ForeignKey('academico.curso.curid'))
    matid = db.Column(db.Integer, db.ForeignKey('academico.materia.matid'))
    periddocente = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'))
    curmatfecini = db.Column(db.Date)
    curmatfecfin = db.Column(db.Date)
    curmatestado = db.Column(db.SmallInteger)
    curmatusureg = db.Column(db.String(50))
    curmatfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    curmatusumod = db.Column(db.String(50))
    curmatfecmod = db.Column(db.DateTime)
    curmatestadodescripcion = db.Column(db.String)
    curmatidrol = db.Column(db.Integer)
    curmatidroldes = db.Column(db.String)
    curmatdescripcion = db.Column(db.String)
    curmatcosto = db.Column(db.Numeric)

    curso = db.relationship('Curso', backref='curso_materias', primaryjoin='CursoMateria.curid == Curso.curid')
    materia = db.relationship('Materia', backref='curso_materias', primaryjoin='CursoMateria.matid == Materia.matid')
    docente = db.relationship('Persona', backref='curso_materias', primaryjoin='CursoMateria.periddocente == Persona.perid')

    def __repr__(self):
        return f'<CursoMateria {self.curmatid}>'

    def to_dict(self):
        return {
            'curmatid': self.curmatid,
            'curid': self.curid,
            'matid': self.matid,
            'periddocente': self.periddocente,
            'curmatfecini': self.curmatfecini.isoformat() if self.curmatfecini else None,
            'curmatfecfin': self.curmatfecfin.isoformat() if self.curmatfecfin else None,
            'curmatestado': self.curmatestado,
            'curmatusureg': self.curmatusureg,
            'curmatfecreg': self.curmatfecreg.isoformat() if self.curmatfecreg else None,
            'curmatusumod': self.curmatusumod,
            'curmatfecmod': self.curmatfecmod.isoformat() if self.curmatfecmod else None,
            'curmatestadodescripcion': self.curmatestadodescripcion,
            'curmatidrol': self.curmatidrol,
            'curmatidroldes': self.curmatidroldes,
            'curmatdescripcion': self.curmatdescripcion,
            'curmatcosto': str(self.curmatcosto) if self.curmatcosto else None
        }
