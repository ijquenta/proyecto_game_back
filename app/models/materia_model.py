from datetime import datetime
from . import db

class Materia(db.Model):
    __tablename__ = 'materia'
    __table_args__ = {'schema': 'academico'}

    matid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matnombre = db.Column(db.String(255), unique=True, nullable=False)
    matusureg = db.Column(db.String(50))
    matfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    matusumod = db.Column(db.String(50))
    matfecmod = db.Column(db.DateTime)
    matestado = db.Column(db.SmallInteger, default=0, nullable=False)
    matnivel = db.Column(db.Integer)
    matdescripcion = db.Column(db.String)
    matestadodescripcion = db.Column(db.String)
    matdesnivel = db.Column(db.String)

    def __repr__(self):
        return f'<Materia {self.matid}>'

    def to_dict(self):
        return {
            'matid': self.matid,
            'matnombre': self.matnombre,
            'matusureg': self.matusureg,
            'matfecreg': self.matfecreg.isoformat() if self.matfecreg else None,
            'matusumod': self.matusumod,
            'matfecmod': self.matfecmod.isoformat() if self.matfecmod else None,
            'matestado': self.matestado,
            'matnivel': self.matnivel,
            'matdescripcion': self.matdescripcion,
            'matestadodescripcion': self.matestadodescripcion,
            'matdesnivel': self.matdesnivel
        }
