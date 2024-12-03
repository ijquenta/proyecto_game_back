from . import db

class TipoPais(db.Model):
    __tablename__ = 'tipo_pais'
    __table_args__ = {'schema': 'academico'}

    paisid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paisnombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<TipoPais {self.paisnombre}>'
