from datetime import datetime
from . import db
from .menu_model import Menu  # Importa Menu explícitamente

class SubMenu(db.Model):
    __tablename__ = 'submenu'
    __table_args__ = {'schema': 'academico'}

    submenid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menid = db.Column(db.Integer, db.ForeignKey('academico.menu.menid'), nullable=False)
    submennombre = db.Column(db.String(50))
    submenusureg = db.Column(db.String(50))
    submenfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    submenusumod = db.Column(db.String(50))
    submenfecmod = db.Column(db.DateTime, default=datetime.utcnow)
    submendescripcion = db.Column(db.String(255))
    submenestado = db.Column(db.SmallInteger, default=1, nullable=False)

    menu = db.relationship('Menu', backref='submenus', primaryjoin='SubMenu.menid == Menu.menid')  # Define la relación

    def __repr__(self):
        return f'<SubMenu {self.submenid}>'

    def to_dict(self):
        return {
            'submenid': self.submenid,
            'menid': self.menid,
            'submennombre': self.submennombre,
            'submenusureg': self.submenusureg,
            'submenfecreg': self.submenfecreg.isoformat() if self.submenfecreg else None,
            'submenusumod': self.submenusumod,
            'submenfecmod': self.submenfecmod.isoformat() if self.submenfecmod else None,
            'submendescripcion': self.submendescripcion,
            'submenestado': self.submenestado
        }
