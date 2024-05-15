# C:\xampp\miapp\usuario\usuario.py
from flask import Blueprint, app, flash, render_template, redirect, request, url_for, session
import os
from werkzeug.utils import secure_filename
import secrets
from confBD import conectionBD
from flask import jsonify

from .forms import RegistroForm
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file


user = Blueprint('user', __name__)

@user.route('/')
def home():
    return render_template('usuario/login.html')

@user.route('/registro', methods=['GET', 'POST'])
def registro():
    from app import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file

    form = RegistroForm()
    msg = '' 
    if form.validate_on_submit():
        cedula = form.cedula.data
        nombres = form.nombres.data
        apellidos = form.apellidos.data
        fnacimiento = form.fnacimiento.data.strftime('%Y-%m-%d')
        print(f"Fecha de nacimiento recibida: {fnacimiento}")
        correo = form.correo.data
        correo2 = form.correo2.data
        cedula_adelante = form.cedula_adelante.data
        cedula_atras = form.cedula_atras.data
        selfie = form.selfie.data

        # crea la carpeta del usuario si no existe
        user_folder_path = os.path.join(UPLOAD_FOLDER, cedula)
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        # Se verifican y guardan los archivos
        if cedula_adelante and allowed_file(cedula_adelante.filename):
            filename = secure_filename(cedula_adelante.filename)
            cedula_adelante_path = os.path.join(user_folder_path, filename)
            cedula_adelante.save(cedula_adelante_path)
        else:
            msg = 'Archivo de cédula adelante no válido'
            return render_template('usuario/registro.html', form=form, msg=msg)

        if cedula_atras and allowed_file(cedula_atras.filename):
            filename = secure_filename(cedula_atras.filename)
            cedula_atras_path = os.path.join(user_folder_path, filename)
            cedula_atras.save(cedula_atras_path)
        else:
            msg = 'Archivo de cédula atrás no válido'
            return render_template('usuario/registro.html', form=form, msg=msg)

        if selfie and allowed_file(selfie.filename):
            filename = secure_filename(selfie.filename)
            selfie_path = os.path.join(user_folder_path, filename)
            selfie.save(selfie_path)
        else:
            msg = 'Archivo de selfie no válido'
            return render_template('usuario/registro.html', form=form, msg=msg)

        # Genera una contraseña temporal
        password_temporal = secrets.token_urlsafe(16)


        user.logger.debug("Formulario validado y procesado")



# Guarda los datos del formulario en la sesión para usarlos en la página de confirmación
        session['datos_formulario'] = {
            'cedula': cedula,
            'nombres': nombres,
            'apellidos': apellidos,
            'fnacimiento': fnacimiento,
            'correo': correo,
            'correo2': correo2,
            'password_temporal': password_temporal
            
        }
        print(session['datos_formulario'])  # Agregar esta línea

# Conexión con la base de datos
        conexion = conectionBD()
        cursor = conexion.cursor()
        
        sql = """INSERT INTO datos (cedula, nombres, apellidos, fnacimiento, correo, estado)
                 VALUES (%s, %s, %s, %s, %s, 'pendiente')"""

        # Ejecutar la consulta
        cursor.execute(sql, (cedula, nombres, apellidos, fnacimiento, correo))
        conexion.commit()

        cursor.close()
        conexion.close()
      
        # Redirigir a la ruta /registro_exitoso
        return redirect(url_for('user.registro_exitoso'))

    # Si la validación del formulario falla, renderizar la plantilla con los errores
    return render_template('usuario/registro.html', form=form, msg=msg)

@user.route('/registro_exitoso', methods=['GET', 'POST'])
def registro_exitoso():
    mensaje = "¡Registro exitoso! Le estaremos enviando un correo de confirmación en la brevedad posible."
    return jsonify({"mensaje": mensaje})

@user.route('/aprobar_archivos/<int:user_id>', methods=['POST'])
def aprobar_archivos(user_id):
    # Se verifica la identidad del administrador y su autorización para aprobar archivos

    # Se obtienen los archivos aprobados del formulario
    cedula_adelante_aprobada = request.files['cedula_adelante_aprobada']
    cedula_atras_aprobada = request.files['cedula_atras_aprobada']
    selfie_aprobada = request.files['selfie_aprobada']

    # Se establece la conexión con la base de datos
    conexion = conectionBD()
    cursor = conexion.cursor()

    # Se actualiza la fila correspondiente en la tabla de la base de datos para incluir los archivos aprobados
    sql = """UPDATE datos SET cedula_adelante_aprobada = %s, cedula_atras_aprobada = %s, selfie_aprobada = %s, estado = 'aprobado' WHERE id = %s"""
    cursor.execute(sql, (cedula_adelante_aprobada.read(), cedula_atras_aprobada.read(), selfie_aprobada.read(), user_id))
    conexion.commit()

    # Se cierra la conexión con la base de datos
    cursor.close()
    conexion.close()

    # Se redirige al administrador a alguna página de confirmación o a la lista de usuarios pendientes de aprobación
    return redirect(url_for('admin.lista_pendientes'))


# Función para registrar el blueprint en la aplicación Flask
def register_user_blueprint(app):
    user.logger = app.logger
    app.register_blueprint(user, url_prefix='/user')



