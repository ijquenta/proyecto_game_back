from datetime import datetime
from . import db

class Menu(db.Model):
    __tablename__ = 'menu'
    __table_args__ = {'schema': 'academico'}

    menid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mennombre = db.Column(db.String(50))
    menicono = db.Column(db.String(50))
    menusureg = db.Column(db.String(50))
    menfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    menusumod = db.Column(db.String(50))
    menfecmod = db.Column(db.DateTime, default=datetime.utcnow)
    mendescripcion = db.Column(db.String(255))
    menestado = db.Column(db.SmallInteger, default=1, nullable=False)

    def __repr__(self):
        return f'<Menu {self.menid}>'

    def to_dict(self):
        return {
            'menid': self.menid,
            'mennombre': self.mennombre,
            'menicono': self.menicono,
            'menusureg': self.menusureg,
            'menfecreg': self.menfecreg.isoformat() if self.menfecreg else None,
            'menusumod': self.menusumod,
            'menfecmod': self.menfecmod.isoformat() if self.menfecmod else None,
            'mendescripcion': self.mendescripcion,
            'menestado': self.menestado
        }