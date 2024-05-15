# app.py
from flask import Flask, request, redirect, session, url_for, render_template
from flask_cors import CORS
from confBD import conectionBD
import mysql.connector
from flask_bcrypt import Bcrypt
from usuario.usuario import user, register_user_blueprint
from admin import admin, register_admin_blueprint
from datetime import timedelta
import logging
#from flask_paginate import Pagination
#from flask import Blueprint
#from usuario.forms import RegistroForm
#import sys
#from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
#from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file





# Inicializa la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'
bcrypt = Bcrypt(app)

# Configurar el nivel de logging
app.logger.setLevel(logging.INFO)

# Acceder al logger de Flask
logger = app.logger

# Configuración de CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


# Registra los Blueprints
register_user_blueprint(app)
register_admin_blueprint(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '')
        password = request.form['password']
        conexion = conectionBD()
        cursor = conexion.cursor(dictionary=True)

        # Retrieve user information based on email and password
        cursor.execute("SELECT id, nombres, apellidos FROM usuarios WHERE correo = %s AND password = %s", (correo, password))
        usuario = cursor.fetchone()

        if usuario:
            user_id = usuario['id']
            nombres = usuario['nombres']
            apellidos = usuario['apellidos']

            # Almacenar los datos del usuario en la sesión
            session['user_id'] = user_id
            session['nombres'] = nombres
            session['apellidos'] = apellidos

            cursor.close()
            conexion.close()

            # Renderizar la plantilla 'inicio_interno.html' y pasar los datos del usuario
            return render_template('admin/inicio_interno.html', datos={'nombres': nombres, 'apellidos': apellidos})
        else:
            cursor.close()
            conexion.close()
            app.logger.error(f"Credenciales incorrectas: correo={correo}, password={password}")
            return render_template('usuario/login.html', error='Credenciales incorrectas')

    return render_template('usuario/login.html')

    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)


