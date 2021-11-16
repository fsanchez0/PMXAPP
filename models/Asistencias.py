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