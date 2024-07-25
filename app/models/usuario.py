from . import db
from models.persona_model import Persona
from models.rol import Rol

class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'academico'}
    usuid = db.Column(db.Integer, primary_key=True)
    perid = db.Column(db.Integer, db.ForeignKey('academico.persona.perid'))
    rolid = db.Column(db.Integer, db.ForeignKey('academico.rol.rolid'))
    usuname = db.Column(db.String(50), nullable=False)
    usupassword = db.Column(db.String(100), nullable=False)
    usupasswordhash = db.Column(db.String, nullable=False)
    usuemail = db.Column(db.String(100), nullable=False)
    usudescripcion = db.Column(db.String(255))
    usuestado = db.Column(db.SmallInteger, default=1)
    usuusureg = db.Column(db.String(50))
    usufecreg = db.Column(db.TIMESTAMP, default=db.func.now())
    usuusumod = db.Column(db.String(50))
    usufecmod = db.Column(db.TIMESTAMP)
    usuconfirmado = db.Column(db.SmallInteger)
    usuconfirmadofecreg = db.Column(db.TIMESTAMP, nullable=True)  # Campo de marca de tiempo para fecha de confirmación
    
    persona = db.relationship('Persona', backref=db.backref('usuarios', lazy=True))
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
    
    def to_dict(self):
        return {
            'usuid': self.usuid,
            'perid': self.perid,
            'pernomcompleto': self.persona.pernomcompleto if self.persona else None,
            'pernrodoc': self.persona.pernrodoc if self.persona else None,
            'perfoto': self.persona.perfoto if self.persona else None,
            'rolid': self.rolid,
            'rolnombre': self.rol.rolnombre if self.rol else None,
            'usuname': self.usuname,
            'usuemail': self.usuemail,
            'usudescripcion': self.usudescripcion,
            'usuestado': self.usuestado,
            'usuusureg': self.usuusureg,
            'usufecreg': self.usufecreg.isoformat() if self.usufecreg else None,
            'usuusumod': self.usuusumod,
            'usufecmod': self.usufecmod.isoformat() if self.usufecmod else None,
            'usuconfirmado': self.usuconfirmado,
            'usuconfirmadofecreg': self.usuconfirmadofecreg
        }
        
    def to_dict_with_persona_rol(self):
        return {
            'usuid': self.usuid,
            'perid': self.perid,
            'rolid': self.rolid,
            'rolnombre': self.rol.rolnombre,
            'usuname': self.usuname,
            'usuemail': self.usuemail,
            'pernomcompleto': self.persona.pernomcompleto if self.persona else None,
            'pernrodoc': self.persona.pernrodoc if self.persona else None,
        }