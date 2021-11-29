from flask import render_template, request, flash, redirect, url_for, send_file, make_response
from flask_login import login_required, current_user
from io import BytesIO
import pandas as pd
import pymssql
import pdfkit

config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
from app.models import Candidato
from app import db
from . import evaluaciones_bp


@evaluaciones_bp.route('/api/data_evaluaciones')
@login_required
def data_evaluaciones():
    query = Candidato.query
    return {
        'data': [candidato.to_dict() for candidato in query]
    }


@evaluaciones_bp.route('/evaluacionesSSE')
@login_required
def evaluaciones():
    return render_template("evaluaciones/home.html")


@evaluaciones_bp.route('/addCandidato')
@login_required
def addRegister():
    return render_template('evaluaciones/addCandidato.html', title='Nuevo Candidato')


@evaluaciones_bp.route('/addCandidato', methods=['POST'])
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
        return redirect(url_for('evaluaciones.evaluaciones'))


@evaluaciones_bp.route('/editCandidato/<id>')
def get_candidato(id):
    candidato = Candidato.query.filter_by(id=id).first()
    return render_template('evaluaciones/editCandidato.html', reg=candidato, title='Editar Registro')


@evaluaciones_bp.route('/updateCandidato/<id>', methods=['POST'])
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
                candidato.f_evaluacion_psic = request.form['f_evaluacion_psic'] + ' ' + request.form['hora_evaluacion_psic']
                candidato.f_evaluacion_piro = request.form['f_evaluacion_piro'] + ' ' + request.form['hora_evaluacion_piro']
                candidato.localizacion_eval = request.form['localizacion_eval']
                db.session.commit()
                flash('Actualizado con éxito')
        except Exception as e:
            flash('Falló al actualizar: ', e)
            print(e)
    return redirect(url_for('evaluaciones.evaluaciones'))


@evaluaciones_bp.route('/deleteCandidato/<id>')
def delete_candidato(id):
    flash('Usuario borrado exitosamente')
    candidato = Candidato.query.filter_by(id=id).first()
    db.session.delete(candidato)
    db.session.commit()
    return redirect(url_for('evaluaciones.evaluaciones'))


@evaluaciones_bp.route('/downloadEval')
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


@evaluaciones_bp.route('/downloadReport')
def downloadReport():
    rendered = render_template('evaluaciones/pdf_template.html')
    pdf = pdfkit.from_string(rendered, False)
    #https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
    #https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachement; filename=output.pdf'

    return response