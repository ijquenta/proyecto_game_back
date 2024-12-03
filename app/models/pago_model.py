from . import db
from datetime import datetime
from sqlalchemy.orm import validates

class Pago(db.Model):
    __tablename__ = 'pago'
    __table_args__ = {'schema': 'academico'}
    pagid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pagdescripcion = db.Column(db.String(255))
    pagmonto = db.Column(db.Numeric(10, 2))
    pagarchivo = db.Column(db.String(255))
    pagusureg = db.Column(db.String(50))
    pagfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    pagusumod = db.Column(db.String(50))
    pagfecmod = db.Column(db.DateTime)
    pagestado = db.Column(db.SmallInteger)
    pagfecha = db.Column(db.Date)  
    pagtipo = db.Column(db.SmallInteger)                            
    
    def __repr__(self):
        return f'<Pago {self.pagid}>'

    def to_dict(self):
        return {
            'pagid': self.pagid,
            'pagdescripcion': self.pagdescripcion,
            'pagmonto': self.pagmonto,
            'pagarchivo': self.pagarchivo,
            'pagfecha': self.pagfecha.isoformat() if self.pagfecha else None,
            'pagusureg': self.pagusureg,
            'pagfecreg': self.pagfecreg.isoformat() if self.pagfecreg else None,
            'pagusumod': self.pagusumod,
            'pagfecmod': self.pagfecmod.isoformat() if self.pagfecmod else None,
            'pagestado': self.pagestado,
            'pagtipo': self.pagtipo
        }
        
class TipoPago(db.Model):
    __tablename__ = 'tipo_pago'
    __table_args__ = {'schema': 'academico'}

    tpagid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tpagnombre = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<TipoPago {self.pagtipnombre}>'