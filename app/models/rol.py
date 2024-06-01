from datetime import datetime
from . import db

class Rol(db.Model):
    __tablename__ = 'rol'
    __table_args__ = {'schema': 'academico'}
    
    rolid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolnombre = db.Column(db.String(50), unique=True, nullable=False)
    roldescripcion = db.Column(db.String(255))
    rolusureg = db.Column(db.String(50))
    rolfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    rolusumod = db.Column(db.String(50))
    rolfecmod = db.Column(db.DateTime)
    rolestado = db.Column(db.SmallInteger, default=1, nullable=False)

    def __repr__(self):
        return f'<Rol {self.rolnombre}>'
    
    def to_dict(self):
        return {
            'rolid': self.rolid,
            'rolnombre': self.rolnombre,
            'roldescripcion': self.roldescripcion,
            'rolusureg': self.rolusureg,
            'rolfecreg': self.rolfecreg.isoformat() if self.rolfecreg else None,
            'rolusumod': self.rolusumod,
            'rolfecmod': self.rolfecmod.isoformat() if self.rolfecmod else None,
            'rolestado': self.rolestado
        }
