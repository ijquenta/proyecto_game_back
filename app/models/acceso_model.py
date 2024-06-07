from datetime import datetime
from . import db

class Acceso(db.Model):
    __tablename__ = 'acceso'
    __table_args__ = (
        db.UniqueConstraint('rolid', 'submenid', name='unique_rol_submen'),
        {'schema': 'academico'}
    )

    accid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolid = db.Column(db.Integer, db.ForeignKey('academico.rol.rolid'))
    submenid = db.Column(db.Integer, db.ForeignKey('academico.submenu.submenid'))
    accactivo = db.Column(db.SmallInteger, default=0)
    accusureg = db.Column(db.String(50))
    accfecreg = db.Column(db.DateTime, default=datetime.now)
    accusumod = db.Column(db.String(50))
    accfecmod = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    accdescripcion = db.Column(db.String(255))
    accestado = db.Column(db.SmallInteger, default=1, nullable=False)

    rol = db.relationship('Rol', backref='accesos')
    submenu = db.relationship('SubMenu', backref='accesos')

    def __repr__(self):
        return f'<Acceso {self.accid}>'

    def to_dict(self):
        return {
            'accid': self.accid,
            'rolid': self.rolid,
            'submenid': self.submenid,
            'accactivo': self.accactivo,
            'accusureg': self.accusureg,
            'accfecreg': self.accfecreg.isoformat() if self.accfecreg else None,
            'accusumod': self.accusumod,
            'accfecmod': self.accfecmod.isoformat() if self.accfecmod else None,
            'accestado': self.accestado
        }
