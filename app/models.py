from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError

from app import db

class Asistencias(db.Model): #Clase Asistencias = Tabla Asistencias
    __tablename__ = 'Asistencias'

    ID = db.Column(db.Integer, nullable=False, primary_key=True)
    NOMBRE = db.Column(db.String(60))
    EDAD = db.Column(db.Integer)
    TELEFONO = db.Column(db.String(15))
    TELEFONO_MOVIL = db.Column(db.String(15))
    CORREO = db.Column(db.String(255))
    FORMACION_ACADEMICA = db.Column(db.String(255))
    CATEGORIA_PROPUESTOS = db.Column(db.String(30))
    ORIGEN = db.Column(db.String(255))
    F_PROGRAMACION = db.Column(db.DATETIME)
    RESPONSABLE = db.Column(db.String(255))
    HORARIO_ESCALONADO = db.Column(db.String(25))
    ID_BT = db.Column(db.Integer)
    TIPO_LICENCIA = db.Column(db.String(255))
    OBS = db.Column(db.String(255))
    PRUEBA_MANEJO = db.Column(db.String(10))
    APTO = db.Column(db.String(10))
    MMPI = db.Column(db.String(10))
    RESULTADO_MMPI = db.Column(db.String(255))
    CAPACITACION_SEGURIDAD = db.Column(db.String(10))
    DOCUMENTACION = db.Column(db.String(10))

    def __repr__(self):
        return "<Nombre: {}>".format(self.NOMBRE)

    def to_dict(self):
        fecha = self.F_PROGRAMACION
        if(self.F_PROGRAMACION is not None):
            fecha = self.F_PROGRAMACION.strftime("%d/%m/%Y")

        return {
            'id': self.ID,
            'nombre': self.NOMBRE,
            'edad': self.EDAD,
            'telefono': self.TELEFONO,
            'telefono_movil': self.TELEFONO_MOVIL,
            'correo': self.CORREO,
            'formacion_academica': self.FORMACION_ACADEMICA,
            'categoria_propuestos': self.CATEGORIA_PROPUESTOS,
            'origen': self.ORIGEN,
            'f_programacion': fecha,
            'responsable': self.RESPONSABLE,
            'horario_escalonado': self.HORARIO_ESCALONADO,
            'id_bt': self.ID_BT,
            'tipo_licencia': self.TIPO_LICENCIA,
            'obs': self.OBS,
            'prueba_manejo': self.PRUEBA_MANEJO,
            'apto': self.APTO,
            'mmpi': self.MMPI,
            'resultado_mmpi': self.RESULTADO_MMPI,
            'capacitacion_seguridad': self.CAPACITACION_SEGURIDAD,
            'documentacion': self.DOCUMENTACION
        }


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
            fecha1 = self.f_evaluacion_psic.strftime("%d/%m/%Y %H:%M")
        if (self.f_evaluacion_piro is not None):
            fecha2 = self.f_evaluacion_piro.strftime("%d/%m/%Y %H:%M")

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
            'f_evaluacion_psic': fecha1,
            'f_evaluacion_piro': fecha2,
            'localizacion_eval': self.localizacion_eval
        }