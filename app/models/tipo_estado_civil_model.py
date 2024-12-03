from . import db

class TipoEstadoCivil(db.Model):
    __tablename__ = 'tipo_estadocivil'
    __table_args__ = {'schema': 'academico'}

    estadocivilid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estadocivilnombre = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<TipoEstadoCivil {self.estadocivilnombre}>'
