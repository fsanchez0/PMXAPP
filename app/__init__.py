from flask_login import LoginManager
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

database_file = "mssql+pymssql://sapp:Pemex.2020*@vwtutsqlp065.un.pemex.com/PEMEX"
engine = create_engine(database_file)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .asistencias import asistencias_bp
    app.register_blueprint(asistencias_bp)

    from .evaluaciones import evaluaciones_bp
    app.register_blueprint(evaluaciones_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    return app


#from .public import public
#app.register_blueprint(public)