from datetime import datetime
from . import db

class Curso(db.Model):
    __tablename__ = 'curso'
    __table_args__ = {'schema': 'academico'}

    curid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curnombre = db.Column(db.String(255))
    curestadodescripcion = db.Column(db.String)
    curnivel = db.Column(db.Integer)
    curfchini = db.Column(db.Date)
    curfchfin = db.Column(db.Date)
    curusureg = db.Column(db.String(50))
    curfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    curusumod = db.Column(db.String(50))
    curfecmod = db.Column(db.DateTime)
    curestado = db.Column(db.SmallInteger)
    curdesnivel = db.Column(db.String(255))
    curdescripcion = db.Column(db.String(250))

    def __repr__(self):
        return f'<Curso {self.curid}>'

    def to_dict(self):
        return {
            'curid': self.curid,
            'curnombre': self.curnombre,
            'curestadodescripcion': self.curestadodescripcion,
            'curnivel': self.curnivel,
            'curfchini': self.curfchini.isoformat() if self.curfchini else None,
            'curfchfin': self.curfchfin.isoformat() if self.curfchfin else None,
            'curusureg': self.curusureg,
            'curfecreg': self.curfecreg.isoformat() if self.curfecreg else None,
            'curusumod': self.curusumod,
            'curfecmod': self.curfecmod.isoformat() if self.curfecmod else None,
            'curestado': self.curestado,
            'curdesnivel': self.curdesnivel,
            'curdescripcion': self.curdescripcion
        }
