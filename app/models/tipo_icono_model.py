from datetime import datetime
from . import db

class TipoIcono(db.Model):
    __tablename__ = 'tipo_icono'
    __table_args__ = {'schema': 'academico'}

    icoid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iconombre = db.Column(db.String(50))

    def __repr__(self):
        return f'<TipoIcono {self.icoid}>'

    def to_dict(self):
        return {
            'icoid': self.icoid,
            'iconombre': self.iconombre,
        }