from . import db

class TipoGenero(db.Model):
    __tablename__ = 'tipo_genero'
    __table_args__ = {'schema': 'academico'}

    generoid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    generonombre = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<TipoGenero {self.generonombre}>'
