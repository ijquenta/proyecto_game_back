from datetime import datetime
from . import db

class Nota(db.Model):
    __tablename__ = 'nota'
    __table_args__ = {'schema': 'academico'}

    notid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    insid = db.Column(db.Integer, unique=True, nullable=True)
    not1 = db.Column(db.Numeric(5, 2), nullable=True)
    not2 = db.Column(db.Numeric(5, 2), nullable=True)
    not3 = db.Column(db.Numeric(5, 2), nullable=True)
    notfinal = db.Column(db.Numeric(5, 2), nullable=True)
    notusureg = db.Column(db.String(50), nullable=True)
    notfecreg = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    notusumod = db.Column(db.String(50), nullable=True)
    notfecmod = db.Column(db.DateTime, nullable=True)
    notestado = db.Column(db.SmallInteger, default=1, nullable=False)

    def __repr__(self):
        return f'<Nota {self.notid}>'

    def to_dict(self):
        return {
            'notid': self.notid,
            'insid': self.insid,
            'not1': float(self.not1) if self.not1 is not None else None,
            'not2': float(self.not2) if self.not2 is not None else None,
            'not3': float(self.not3) if self.not3 is not None else None,
            'notfinal': float(self.notfinal) if self.notfinal is not None else None,
            'notusureg': self.notusureg,
            'notfecreg': self.notfecreg.isoformat() if self.notfecreg else None,
            'notusumod': self.notusumod,
            'notfecmod': self.notfecmod.isoformat() if self.notfecmod else None,
            'notestado': self.notestado
        }
