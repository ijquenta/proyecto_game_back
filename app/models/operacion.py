from datetime import datetime
from . import db
  
class Operacion(db.Model):
    __tablename__ = 'operacion'
    __table_args__ = {'schema': 'academico'}
    
    opeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openombre = db.Column(db.String(50))
    opeusureg = db.Column(db.String(50))
    opefecreg = db.Column(db.DateTime, default=datetime.utcnow)
    opeusumod = db.Column(db.String(50))
    opefecmod = db.Column(db.DateTime, default=datetime.utcnow)
    opedescripcion = db.Column(db.String(255))
    opeestado = db.Column(db.SmallInteger, default=1, nullable=False)

    def __repr__(self):
        return f'<Operacion {self.opeid}>'
    
    def to_dict(self):
        
        return {
            'opeid': self.opeid,
            'openombre': self.openombre,
            'opeusureg': self.opeusureg,
            'opefecreg': self.opefecreg.isoformat() if self.opefecreg else None,
            'opeusumod': self.opeusumod,
            'opefecmod': self.opefecmod.isoformat() if self.opefecmod else None,
            'opedescripcion': self.opedescripcion,
            'opeestado': self.opeestado
        }
