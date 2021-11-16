from sqlalchemy.orm import relationship

from app import db


class Candidato(db.Model):
    __tablename__ = 'tb_candidato'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer)
    id_bt = db.Column(db.Integer)
    motivo_evaluacion = db.Column(db.String(30))
    formacion_academica = db.Column(db.String(20))
    puesto = db.Column(db.String(100))
    centro_trabajo = db.Column(db.String(100))
    estado_civil = db.Column(db.String(10))
    #programacion_evaluacion = relationship("ProgramacionEvaluacion", uselist=False, backref="candidato")

    def __repr__(self):
        return f'Candidato {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Candidato.query.get(id)
