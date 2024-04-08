from flask import Blueprint, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
from confBD import conectionBD
from email_utils import enviar_correo

interno = Blueprint('interno', __name__, template_folder='templates/interno')

@interno.route('/confirmar_datos', methods=['GET', 'POST'])
def confirmar_datos():
    if request.method == 'POST':
        # Obtener los datos del formulario de confirmación
        nombres_confirmados = request.form['nombres']
        apellidos_confirmados = request.form['apellidos']
        cedula_confirmada = request.form['cedula']
        fnacimiento_confirmado = request.form['fnacimiento']
        print(f"Datos recibidos: {nombres_confirmados}, {apellidos_confirmados}, {cedula_confirmada}, {fnacimiento_confirmado}")


        # Verificar si los datos coinciden con los de la sesión
        if (nombres_confirmados == session['datos_formulario']['nombres'] and
            apellidos_confirmados == session['datos_formulario']['apellidos'] and
            cedula_confirmada == session['datos_formulario']['cedula'] and
            fnacimiento_confirmado == session['datos_formulario']['fnacimiento']):
            print(f"Fecha de nacimiento en la sesión: {session['datos_formulario']['fnacimiento']}")


            # Guardar los datos en la base de datos
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor(dictionary=True)

            sql = "INSERT INTO datos (cedula, nombres, apellidos, fnacimiento, correo, correo2, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, NOW())"
            valores = (cedula_confirmada, nombres_confirmados, apellidos_confirmados, fnacimiento_confirmado, session['datos_formulario']['correo'], session['datos_formulario']['correo2'])
            cursor.execute(sql, valores)
            conexion_MySQL.commit()

            cursor.close()
            conexion_MySQL.close()

            return redirect(url_for('confirmacion_exitosa'))
        else:
            msg = 'La información en el formulario no coincide con los datos confirmados'
            return render_template('interno/datos_confirmar.html', msg=msg)
    else:
        return render_template('interno/datos_confirmar.html', datos=session['datos_formulario'])
    
@interno.route('/enviar_correo_confirmacion', methods=['POST'])
def enviar_correo_confirmacion():
    if 'datos_formulario' in session:
        enviar_correo(session['datos_formulario']['correo'], session['datos_formulario']['password_temporal'])
        return 'Correo electrónico enviado exitosamente'
    else:
        return 'No hay datos de formulario en la sesión'

@interno.route('/confirmar_datos', methods=['GET', 'POST'])
def confirmar_datos():
    if request.method == 'POST':
        # Obtener los datos del formulario de confirmación
        nombres_confirmados = request.form['nombres']
        apellidos_confirmados = request.form['apellidos']
        cedula_confirmada = request.form['cedula']
        fnacimiento_confirmado = request.form['fnacimiento']
        print(f"Datos recibidos: {nombres_confirmados}, {apellidos_confirmados}, {cedula_confirmada}, {fnacimiento_confirmado}")


        # Verificar si los datos coinciden con los de la sesión
        if (nombres_confirmados == session['datos_formulario']['nombres'] and
            apellidos_confirmados == session['datos_formulario']['apellidos'] and
            cedula_confirmada == session['datos_formulario']['cedula'] and
            fnacimiento_confirmado == session['datos_formulario']['fnacimiento']):
            print(f"Fecha de nacimiento en la sesión: {session['datos_formulario']['fnacimiento']}")


            # Guardar los datos en la base de datos
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor(dictionary=True)

            sql = "INSERT INTO datos (cedula, nombres, apellidos, fnacimiento, correo, correo2, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, NOW())"
            valores = (cedula_confirmada, nombres_confirmados, apellidos_confirmados, fnacimiento_confirmado, session['datos_formulario']['correo'], session['datos_formulario']['correo2'])
            cursor.execute(sql, valores)
            conexion_MySQL.commit()

            cursor.close()
            conexion_MySQL.close()

            return redirect(url_for('confirmacion_exitosa'))
        else:
            msg = 'La información en el formulario no coincide con los datos confirmados'
            return render_template('interno/datos_confirmar.html', msg=msg)
    else:
        return render_template('interno/datos_confirmar.html', datos=session['datos_formulario'])

@interno.route('/')
def home():
    return render_template('externo/login.html')

if __name__ == '__main__':
    interno.run(debug=True, host='0.0.0.0', port=5000, threaded=True)