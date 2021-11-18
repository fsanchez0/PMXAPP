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
    f_evaluacion_psic = db.Column(db.DATETIME)  # Fecha y Hora
    f_evaluacion_piro = db.Column(db.DATETIME)  # Fecha y Hora
    localizacion_eval = db.Column(db.String(100))
    #motivo_evaluacion = db.Column(db.String(30))

    def __repr__(self):
        return "<Nombre: {}>".format(self.nombre)

    def save(self): #creo que no se usa
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Candidato.query.get(id)

    def to_dict(self):
        fecha1 = self.f_evaluacion_psic
        fecha2 = self.f_evaluacion_piro
        if(self.f_evaluacion_psic is not None):
            fecha1 = self.f_evaluacion_psic.strftime("%d/%m/%Y")
        if (self.f_evaluacion_piro is not None):
            fecha2 = self.f_evaluacion_piro.strftime("%d/%m/%Y")

        return {
            'id': self.id,
            'nombre': self.nombre,
            'edad': self.edad,
            'id_bt': self.id_bt,
            'motivo_evaluacion': self.motivo_evaluacion,
            'formacion_academica': self.formacion_academica,
            'puesto': self.puesto,
            'centro_trabajo': self.centro_trabajo,
            'estado_civil': self.estado_civil,
            'f_evaluacion_psic': self.f_evaluacion_psic,
            'f_evaluacion_piro': self.f_evaluacion_piro,
            'localizacion_eval': self.localizacion_eval
        }