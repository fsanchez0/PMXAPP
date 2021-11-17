from flask_login import LoginManager, login_manager, current_user, login_user, login_required
from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.urls import url_parse
from forms import LoginForm
from waitress import serve
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "mssql+pymssql://sapp:Pemex.2020*@vwtutsqlp065.un.pemex.com/PEMEX"
engine = create_engine(database_file)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
app = Flask(__name__)

app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
from models.User import Usuario
from models.Asistencias import Asistencias
from models import Candidato
login_manager = LoginManager(app)


@app.route('/')
def home():  # put application's code here
    return render_template("index.html")


@app.route('/asistencias', methods=["GET", "POST"])
def homeAsistencias():
    return render_template("asistencias/home.html", title='Inicio Asistencias')


@app.route('/api/data')
def data():
    query = Asistencias.query
    return {
        'data': [asistencia.to_dict() for asistencia in query]
    }


@app.route('/evaluacionesSSE')
def evaluaciones():
    return render_template("evaluaciones.html")


@app.route('/addCandidato')
def addRegister():
    return render_template('addCandidato.html', title='Nuevo Candidato')


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


Base.metadata.create_all(db.engine)
serve(app, host='0.0.0.0', port=8080, threads=1)
#app.run()
