from . import db
from datetime import datetime
from sqlalchemy.orm import validates

class ToDictMixin:
    @validates('*')
    def to_dict_impl(self, key, value):
        if isinstance(value, datetime.date):
            return value.isoformat()
        return value

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class modelPago(db.Model, ToDictMixin):
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