from datetime import datetime
from . import db

class TipoMatricula(db.Model):
    __tablename__ = 'tipo_matricula'
    __table_args__ = {'schema': 'academico'}

    tipmatrid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipmatrgestion = db.Column(db.String)
    tipmatrfecini = db.Column(db.Date)
    tipmatrfecfin = db.Column(db.Date)
    tipmatrcosto = db.Column(db.Numeric)
    tipmatrusureg = db.Column(db.String(50))
    tipmatrfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    tipmatrusumod = db.Column(db.String(50))
    tipmatrfecmod = db.Column(db.DateTime)
    tipmatrestado = db.Column(db.Integer)
    tipmatrdescripcion = db.Column(db.String(255))

    def __repr__(self):
        return f'<TipoMatricula {self.tipmatrid}>'

    def to_dict(self):
        return {
            'tipmatrid': self.tipmatrid,
            'tipmatrgestion': self.tipmatrgestion,
            'tipmatrfecini': self.tipmatrfecini.isoformat() if self.tipmatrfecini else None,
            'tipmatrfecfin': self.tipmatrfecfin.isoformat() if self.tipmatrfecfin else None,
            'tipmatrcosto': str(self.tipmatrcosto) if self.tipmatrcosto else None,
            'tipmatrusureg': self.tipmatrusureg,
            'tipmatrfecreg': self.tipmatrfecreg.isoformat() if self.tipmatrfecreg else None,
            'tipmatrusumod': self.tipmatrusumod,
            'tipmatrfecmod': self.tipmatrfecmod.isoformat() if self.tipmatrfecmod else None,
            'tipmatrestado': self.tipmatrestado,
            'tipmatrdescripcion': self.tipmatrdescripcion
        }
