from sqlalchemy import ForeignKey

from app import db


class ProgramacionEvaluacion(db.Model):
    __tablename__ = 'tb_prog_evaluaciones'

    id = db.Column(db.Integer, primary_key=True)
    f_evaluacion_psic = db.Column(db.DATETIME) #Fecha y Hora
    f_evaluacion_piro = db.Column(db.DATETIME) #Fecha y Hora
    localizacion_eval = db.Column(db.String(100))
    motivo_evaluacion = db.Column(db.String(30))
    #candidato = db.Column(db.Integer, ForeignKey('candidato.id'))

    def __repr__(self):
        return f'<ProgramacionEvaluaciones {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_by_id(id):
        return ProgramacionEvaluacion.query.get(id)
