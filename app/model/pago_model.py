from core.config import db
from datetime import datetime

class modelPago(db.Model):
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
    pagfecha = db.Column(db.Date)  # Ajuste: Corregido el orden de la columna pagfecha
    pagtipo = db.Column(db.SmallInteger)