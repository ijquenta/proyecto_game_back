from datetime import datetime
from . import db
  
class Permiso(db.Model):
    __tablename__ = 'permiso'
    __table_args__ = {'schema': 'academico'}
    
    permid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolid = db.Column(db.Integer, db.ForeignKey('academico.rol.rolid'))
    opeid = db.Column(db.Integer, db.ForeignKey('academico.operacion.opeid'))
    permactivo = db.Column(db.SmallInteger, default=0)
    permusureg = db.Column(db.String(50))
    permfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    permusumod = db.Column(db.String(50))
    permfecmod = db.Column(db.DateTime, default=datetime.utcnow)
    permdescripcion = db.Column(db.String(255))
    permestado = db.Column(db.SmallInteger, default=1, nullable=False)
    rol = db.relationship('Rol', backref='permisos')
    operacion = db.relationship('Operacion', backref='permisos')

    def __repr__(self):
        return f'<Permiso {self.permid}>'
    
    def to_dict(self):
        return {
            'permid': self.permid,
            'rolid': self.rolid,
            'opeid': self.opeid,
            'permactivo': self.permactivo,
            'permusureg': self.permusureg,
            'permfecreg': self.permfecreg.isoformat() if self.permfecreg else None,
            'permusumod': self.permusumod,
            'permfecmod': self.permfecmod.isoformat() if self.permfecmod else None,
            'permestado': self.permestado
        }
