from . import db

class TipoCiudad(db.Model):
    __tablename__ = 'tipo_ciudad'
    __table_args__ = {'schema': 'academico'}

    ciudadid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ciudadnombre = db.Column(db.String(100), nullable=False)
    paisid = db.Column(db.Integer, db.ForeignKey('academico.tipo_pais.paisid'), nullable=False)

    tipo_pais = db.relationship('TipoPais', backref=db.backref('ciudades', lazy=True))

    def __repr__(self):
        return f'<TipoCiudad {self.ciudadnombre}>'
