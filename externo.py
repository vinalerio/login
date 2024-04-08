# externo.py
from flask import Blueprint, render_template, redirect, request, url_for, session
from forms import RegistrationForm
import os
from werkzeug.utils import secure_filename
import secrets

externo = Blueprint('externo', __name__, template_folder='templates/externo')

@externo.route('/')
def home():
    return render_template('login.html')

@externo.route('/register', methods=['GET', 'POST'])
def registro():
    from app import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file

    form = RegistrationForm()
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

        # Manejo de archivos
        user_folder_path = os.path.join(UPLOAD_FOLDER, cedula)
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        if cedula_adelante and allowed_file(cedula_adelante.filename):
            filename = secure_filename(cedula_adelante.filename)
            cedula_adelante_path = os.path.join(user_folder_path, filename)
            cedula_adelante.save(cedula_adelante_path)
        else:
            msg = 'Archivo de cédula adelante no válido'
            return render_template('externo/registro.html', form=form, msg=msg)

        if cedula_atras and allowed_file(cedula_atras.filename):
            filename = secure_filename(cedula_atras.filename)
            cedula_atras_path = os.path.join(user_folder_path, filename)
            cedula_atras.save(cedula_atras_path)
        else:
            msg = 'Archivo de cédula atrás no válido'
            return render_template('externo/registro.html', form=form, msg=msg)

        if selfie and allowed_file(selfie.filename):
            filename = secure_filename(selfie.filename)
            selfie_path = os.path.join(user_folder_path, filename)
            selfie.save(selfie_path)
        else:
            msg = 'Archivo de selfie no válido'
            return render_template('externo/registro.html', form=form, msg=msg)

        # Genera una contraseña temporal
        password_temporal = secrets.token_urlsafe(16)

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


        # Envía un correo electrónico al cliente con la contraseña temporal
        #enviar_correo(correo, password_temporal)
        
        # Después de guardar los datos en la base de datos
        #enviar_correo(session['datos_formulario']['correo'], session['datos_formulario']['password_temporal'])

        # Redirige al usuario a la página de confirmación
        return redirect(url_for('confirmar_datos'))
    else:
        if request.method == 'POST':
            msg = 'Método HTTP incorrecto'
        return render_template('externo/registro.html', form=form, msg=msg)