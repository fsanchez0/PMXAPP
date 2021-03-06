from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Usuario(db.Model, UserMixin):
    __tablename__ = 'tb_usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    cedulaProfesional = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def es_admin(self):
        return self.is_admin

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()