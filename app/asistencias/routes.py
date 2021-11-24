from flask import render_template, redirect, url_for, send_file, request, flash
from flask_login import login_required, current_user
from io import BytesIO
import pandas as pd
import pymssql


from app.models import Asistencias
from app import db
from . import asistencias_bp


@asistencias_bp.route('/asistencias', methods=["GET", "POST"])
@login_required
def home():
    return render_template("asistencias/home.html", title='Inicio Asistencias')


@asistencias_bp.route('/api/data')
@login_required
def data():
    query = Asistencias.query
    return {
        'data': [asistencia.to_dict() for asistencia in query]
    }


@asistencias_bp.route('/download')
@login_required
def download():
    g_connect = pymssql.connect('vwtutsqlp065.un.pemex.com', 'sapp', 'Pemex.2020*', 'PEMEX')
    sql_query = pd.read_sql_query('''SELECT * FROM Asistencias''', g_connect)
    # create a random Pandas dataframe
    df = pd.DataFrame(sql_query)
    df["F_PROGRAMACION"] = df["F_PROGRAMACION"].dt.strftime("%d/%m/%Y")
    # create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    df.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Asistencias", index=False)
    workBook = writer.book
    workSheet = writer.sheets["Asistencias"]
    # the writer has done its job
    writer.close()
    # go back to the beginning of the stream
    output.seek(0)
    return send_file(output, attachment_filename="Asistencias.xlsx", as_attachment=True)



@asistencias_bp.route('/addReg')
@login_required
def addRegister():
    return render_template('asistencias/addReg.html', title='Nuevo Registro')


@asistencias_bp.route('/addReg', methods=['POST'])
@login_required
def add_register():
    if request.method == 'POST':
        if request.form:
            try:
                asistencia = Asistencias()
                asistencia.NOMBRE = request.form['NOMBRE']
                asistencia.EDAD = request.form['EDAD']
                asistencia.TELEFONO = request.form['TELEFONO']
                asistencia.TELEFONO_MOVIL = request.form['TELEFONO_MOVIL']
                asistencia.CORREO = request.form['CORREO']
                asistencia.FORMACION_ACADEMICA = request.form['FORMACION_ACADEMICA']
                asistencia.CATEGORIA_PROPUESTOS = request.form['CATEGORIA_PROPUESTOS']
                asistencia.ORIGEN = request.form['ORIGEN']
                asistencia.F_PROGRAMACION = request.form['F_PROGRAMACION']
                asistencia.RESPONSABLE = request.form['RESPONSABLE']
                asistencia.HORARIO_ESCALONADO = request.form['HORARIO_ESCALONADO']
                asistencia.ID_BT = request.form['ID_BT']
                asistencia.TIPO_LICENCIA = request.form['TIPO_LICENCIA']
                asistencia.OBS = request.form['OBS']
                asistencia.PRUEBA_MANEJO = request.form['PRUEBA_MANEJO']
                asistencia.APTO = request.form['APTO']
                asistencia.MMPI = request.form['MMPI']
                asistencia.RESULTADO_MMPI = request.form['RESULTADO_MMPI']
                asistencia.CAPACITACION_SEGURIDAD = request.form['CAPACITACION_SEGURIDAD']
                asistencia.DOCUMENTACION = request.form['DOCUMENTACION']
                db.session.add(asistencia)
                db.session.commit()
                flash('Usuario agregado exitosamente')
            except Exception as e:
                flash('Falló al agregar: ', e)
                print(e)
        return redirect(url_for('asistencias.home'))


@asistencias_bp.route('/editReg/<id>')
@login_required
def get_register(id):
    asistencia = Asistencias.query.filter_by(ID=id).first()
    return render_template('asistencias/editReg.html', reg=asistencia, title='Editar Registro')


@asistencias_bp.route('/updateReg/<id>', methods=['POST'])
@login_required
def updateReg(id):
    print("Voy a actualizar: ", Asistencias.query.filter_by(ID=id).first())
    if request.method == 'POST':
        try:
            asistencia = Asistencias.query.filter_by(ID=id).first()
            if asistencia is not None:
                asistencia.NOMBRE = request.form['NOMBRE']
                asistencia.EDAD = request.form['EDAD']
                asistencia.TELEFONO = request.form['TELEFONO']
                asistencia.TELEFONO_MOVIL = request.form['TELEFONO_MOVIL']
                asistencia.CORREO = request.form['CORREO']
                asistencia.FORMACION_ACADEMICA = request.form['FORMACION_ACADEMICA']
                asistencia.CATEGORIA_PROPUESTOS = request.form['CATEGORIA_PROPUESTOS']
                asistencia.ORIGEN = request.form['ORIGEN']
                asistencia.F_PROGRAMACION = request.form['F_PROGRAMACION']
                asistencia.RESPONSABLE = request.form['RESPONSABLE']
                asistencia.HORARIO_ESCALONADO = request.form['HORARIO_ESCALONADO']
                asistencia.ID_BT = request.form['ID_BT']
                asistencia.TIPO_LICENCIA = request.form['TIPO_LICENCIA']
                asistencia.OBS = request.form['OBS']
                asistencia.PRUEBA_MANEJO = request.form['PRUEBA_MANEJO']
                asistencia.APTO = request.form['APTO']
                asistencia.MMPI = request.form['MMPI']
                asistencia.RESULTADO_MMPI = request.form['RESULTADO_MMPI']
                asistencia.CAPACITACION_SEGURIDAD = request.form['CAPACITACION_SEGURIDAD']
                asistencia.DOCUMENTACION = request.form['DOCUMENTACION']
                db.session.commit()
                flash('Actualizado con éxito')
        except Exception as e:
            flash('Falló al actualizar: ', e)
            print(e)
    return redirect(url_for('asistencias.home'))


@asistencias_bp.route('/deleteReg/<id>')
@login_required
def delete_register(id):
    flash('Usuario borrado exitosamente')
    asistencia = Asistencias.query.filter_by(ID=id).first()
    db.session.delete(asistencia)
    db.session.commit()
    return redirect(url_for('asistencias.home'))

