from . import db

class TipoDocumento(db.Model):
    __tablename__ = 'tipo_documento'
    __table_args__ = {'schema': 'academico'}

    tipodocid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipodocnombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<TipoDocumento {self.tipodocnombre}>'
