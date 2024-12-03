from datetime import datetime
from . import db


class TipoTexto(db.Model):
    __tablename__ = 'tipo_texto'
    __table_args__ = {'schema': 'academico'}
    
    tiptexid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tiptexnombre = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<TipoTexto {self.tiptexnombre}>'
    
    def to_dict(self):
        return {
            'tiptexid': self.tiptexid,
            'tiptexnombre': self.tiptexnombre
        }
        
# Modelo para tipo_idioma_texto
class TipoIdiomaTexto(db.Model):
    __tablename__ = 'tipo_idioma_texto'
    __table_args__ = {'schema': 'academico'}
    
    tipidiid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipidinombre = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<TipoIdiomaTexto {self.tipidinombre}>'
    
    def to_dict(self):
        return {
            'tipidiid': self.tipidiid,
            'tipidinombre': self.tipidinombre
        }

# Modelo para tipo_categoria_texto
class TipoCategoriaTexto(db.Model):
    __tablename__ = 'tipo_categoria_texto'
    __table_args__ = {'schema': 'academico'}
    
    tipcatid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipcatnombre = db.Column(db.String(255), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<TipoCategoriaTexto {self.tipcatnombre}>'
    
    def to_dict(self):
        return {
            'tipcatid': self.tipcatid,
            'tipcatnombre': self.tipcatnombre
        }

# Modelo para tipo_extension_texto
class TipoExtensionTexto(db.Model):
    __tablename__ = 'tipo_extension_texto'
    __table_args__ = {'schema': 'academico'}
    
    tipextid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipextnombre = db.Column(db.String(10), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<TipoExtensionTexto {self.tipextnombre}>'
    
    def to_dict(self):
        return {
            'tipextid': self.tipextid,
            'tipextnombre': self.tipextnombre
        }

# Modelo para texto
class Texto(db.Model):
    __tablename__ = 'texto'
    __table_args__ = {'schema': 'academico'}
    
    texid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texnombre = db.Column(db.String(255), nullable=False)
    textipo = db.Column(db.Integer, db.ForeignKey('academico.tipo_texto.tiptexid'))
    texformato = db.Column(db.Integer) 
    texdocumento = db.Column(db.String(255))
    texruta = db.Column(db.String(255))
    texdescripcion = db.Column(db.Text)
    texautor = db.Column(db.String(255))
    texsize = db.Column(db.BigInteger)
    texextension = db.Column(db.Integer, db.ForeignKey('academico.tipo_extension_texto.tipextid'))
    texidioma = db.Column(db.Integer, db.ForeignKey('academico.tipo_idioma_texto.tipidiid'))
    texfecpublicacion = db.Column(db.Date)
    texcategoria = db.Column(db.Integer, db.ForeignKey('academico.tipo_categoria_texto.tipcatid'))
    texusureg = db.Column(db.String(50))
    texfecreg = db.Column(db.DateTime, default=datetime.utcnow)
    texusumod = db.Column(db.String(50))
    texfecmod = db.Column(db.DateTime)
    texestado = db.Column(db.SmallInteger, default=1, nullable=False)

    def __repr__(self):
        return f'<Texto {self.texnombre}>'
    
    def to_dict(self):
        return {
            'texid': self.texid,
            'texnombre': self.texnombre,
            'textipo': self.textipo,
            'texformato': self.texformato,
            'texdocumento': self.texdocumento,
            'texruta': self.texruta,
            'texdescripcion': self.texdescripcion,
            'texautor': self.texautor,
            'texsize': self.texsize,
            'texextension': self.texextension,
            'texidioma': self.texidioma,
            'texfecpublicacion': self.texfecpublicacion.isoformat() if self.texfecpublicacion else None,
            'texcategoria': self.texcategoria,
            'texusureg': self.texusureg,
            'texfecreg': self.texfecreg.isoformat() if self.texfecreg else None,
            'texusumod': self.texusumod,
            'texfecmod': self.texfecmod.isoformat() if self.texfecmod else None,
            'texestado': self.texestado
        }

# Modelo para materia_texto
class MateriaTexto(db.Model):
    __tablename__ = 'materia_texto'
    __table_args__ = {'schema': 'academico'}
    
    mattexid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matid = db.Column(db.Integer, nullable=False)
    texid = db.Column(db.Integer, nullable=False)
    mattexdescripcion = db.Column(db.String)
    mattexusureg = db.Column(db.String)
    mattexfecreg = db.Column(db.DateTime)
    mattexusumod = db.Column(db.String)
    mattexfecmod = db.Column(db.DateTime)
    mattexestado = db.Column(db.SmallInteger, default=1)
    
    def __repr__(self):
        return f'<MateriaTexto {self.matid}-{self.texid}>'
    
    def to_dict(self):
        return {
            'mattexid': self.mattexid,
            'matid': self.matid,
            'texid': self.texid,
            'mattexdescripcion': self.mattexdescripcion,
            'mattexusureg': self.mattexusureg,
            'mattexfecreg': self.mattexfecreg.isoformat() if self.mattexfecreg else None,
            'mattexusumod': self.mattexusumod,
            'mattexfecmod': self.mattexfecmod.isoformat() if self.mattexfecmod else None,
            'mattexestado': self.mattexestado
        }