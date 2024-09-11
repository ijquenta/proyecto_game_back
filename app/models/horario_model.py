from . import db
from datetime import datetime

class Horario(db.Model):
    __tablename__ = 'horario'
    __table_args__ = {'schema': 'academico'}
    
    horid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curmatid = db.Column(db.Integer, db.ForeignKey('academico.curso_materia.curmatid'), nullable=False)
    hordia = db.Column(db.String(2), nullable=False)
    horini = db.Column(db.Time, nullable=False)
    horfin = db.Column(db.Time, nullable=False)
    horfecini = db.Column(db.Date, nullable=False)
    horfecfin = db.Column(db.Date, nullable=False)
    horusureg = db.Column(db.String(50))
    horfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    horusumod = db.Column(db.String(50))
    horfecmod = db.Column(db.DateTime)
    horestado = db.Column(db.SmallInteger)
    
    curso_materia = db.relationship('CursoMateria', backref=db.backref('horarios', lazy=True))
    
    def __repr__(self):
        return f'<Horario {self.horid}>'

    def to_dict(self):
        return {
            'horid': self.horid,
            'curmatid': self.curmatid,
            'hordia': self.hordia,
            'horini': self.horini.isoformat() if self.horini else None,
            'horfin': self.horfin.isoformat() if self.horfin else None,
            'horfecini': self.horfecini.isoformat() if self.horfecini else None,
            'horfecfin': self.horfecfin.isoformat() if self.horfecfin else None,
            'horusureg': self.horusureg,
            'horfecreg': self.horfecreg.isoformat() if self.horfecreg else None,
            'horusumod': self.horusumod,
            'horfecmod': self.horfecmod.isoformat() if self.horfecmod else None,
            'horestado': self.horestado
        }
