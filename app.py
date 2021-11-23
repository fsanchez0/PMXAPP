from flask_login import LoginManager, login_manager, current_user, login_user, login_required, logout_user
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.urls import url_parse
from forms import LoginForm, SignupForm
from waitress import serve
from io import BytesIO
import pandas as pd
import xlsxwriter
import pymssql
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
from models.Usuario import Usuario
from models.Asistencias import Asistencias
from models.Candidato import Candidato
login_manager = LoginManager(app)


@app.route('/')
@login_required
def home():  # put application's code here
    return render_template("index.html")


@app.route('/asistencias', methods=["GET", "POST"])
@login_required
def homeAsistencias():
    return render_template("asistencias/home.html", title='Inicio Asistencias')


@app.route('/api/data')
@login_required
def data():
    query = Asistencias.query
    return {
        'data': [asistencia.to_dict() for asistencia in query]
    }


@app.route('/api/data_evaluaciones')
@login_required
def data_evaluaciones():
    query = Candidato.query
    return {
        'data': [candidato.to_dict() for candidato in query]
    }


@app.route('/evaluacionesSSE')
@login_required
def evaluaciones():
    return render_template("evaluaciones/home.html")


@app.route('/addCandidato')
@login_required
def addRegister():
    return render_template('evaluaciones/addCandidato.html', title='Nuevo Candidato')


@app.route('/addCandidato', methods=['POST'])
def add_candidato():
    if request.method == 'POST':
        if request.form:
            try:
                candidato = Candidato()
                candidato.nombre = request.form['nombre']
                candidato.edad = request.form['edad']
                candidato.id_bt = request.form['id_bt']
                candidato.motivo_evaluacion = request.form['motivo_evaluacion']
                candidato.formacion_academica = request.form['formacion_academica']
                candidato.puesto = request.form['puesto']
                candidato.centro_trabajo = request.form['centro_trabajo']
                candidato.estado_civil = request.form['estado_civil']
                candidato.f_evaluacion_psic = request.form['f_evaluacion_psic'] + ' ' + request.form['hora_evaluacion_psic']
                candidato.f_evaluacion_piro = request.form['f_evaluacion_piro'] + ' ' + request.form['hora_evaluacion_piro']
                candidato.localizacion_eval = request.form['localizacion_eval']
                db.session.add(candidato)
                db.session.commit()
                flash('Usuario agregado exitosamente')
            except Exception as e:
                flash('Falló al agregar: ', e)
                print(e)
        return redirect(url_for('evaluaciones'))


@app.route('/editCandidato/<id>')
def get_candidato(id):
    candidato = Candidato.query.filter_by(id=id).first()
    return render_template('evaluaciones/editCandidato.html', reg=candidato, title='Editar Registro')


@app.route('/updateCandidato/<id>', methods=['POST'])
def updateCandidato(id):
    print("Voy a actualizar: ", Candidato.query.filter_by(id=id).first())
    if request.method == 'POST':
        try:
            candidato = Candidato.query.filter_by(id=id).first()
            if candidato is not None:
                candidato.nombre = request.form['nombre']
                candidato.edad = request.form['edad']
                candidato.id_bt = request.form['id_bt']
                candidato.motivo_evaluacion = request.form['motivo_evaluacion']
                candidato.formacion_academica = request.form['formacion_academica']
                candidato.puesto = request.form['puesto']
                candidato.centro_trabajo = request.form['centro_trabajo']
                candidato.estado_civil = request.form['estado_civil']
                candidato.f_evaluacion_psic = request.form['f_evaluacion_psic']
                candidato.f_evaluacion_piro = request.form['f_evaluacion_piro']
                candidato.localizacion_eval = request.form['localizacion_eval']
                db.session.commit()
                flash('Actualizado con éxito')
        except Exception as e:
            flash('Falló al actualizar: ', e)
            print(e)
    return redirect(url_for('evaluaciones'))


@app.route('/deleteCandidato/<id>')
def delete_candidato(id):
    flash('Usuario borrado exitosamente')
    candidato = Candidato.query.filter_by(id=id).first()
    db.session.delete(candidato)
    db.session.commit()
    return redirect(url_for('evaluaciones'))


@app.route('/downloadEval')
def downloadEval():
    g_connect = pymssql.connect('vwtutsqlp065.un.pemex.com', 'sapp', 'Pemex.2020*', 'PEMEX')
    sql_query = pd.read_sql_query('''SELECT * FROM tb_candidato''', g_connect)
    # create a random Pandas dataframe
    df = pd.DataFrame(sql_query)
    df["f_evaluacion_psic"] = df["f_evaluacion_psic"].dt.strftime("%d/%m/%Y")
    df["f_evaluacion_piro"] = df["f_evaluacion_piro"].dt.strftime("%d/%m/%Y")
    # create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    df.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Candidatos", index=False)
    workBook = writer.book
    workSheet = writer.sheets["Candidatos"]
    # the writer has done its job
    writer.close()
    # go back to the beginning of the stream
    output.seek(0)
    return send_file(output, attachment_filename="Candidatos.xlsx", as_attachment=True)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuario.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(nombre=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)


#Base.metadata.create_all(db.engine)
serve(app, host='0.0.0.0', port=8080, threads=1)
#app.run()
