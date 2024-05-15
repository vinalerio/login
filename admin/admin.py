    #  C:\xampp\miapp\admin\admin.py
from flask import Blueprint, render_template, request, url_for, redirect, session, jsonify
from flask_mysqldb import MySQL
    #from flask_login import login_required
    #from flask_login import current_user
from confBD import conectionBD
#from models import Imagen
#from config import miapp
    #import logging
from email_utils import enviar_correo
import secrets
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime, date




admin = Blueprint('admin', __name__)



    # Configuración de paginación
Paginas = 10  # Número de elementos por página

def format_date(value, format='%Y-%m-%d'):
        if isinstance(value, date):
            return value.strftime(format)
        else:
            return ''

@admin.route('/inicio_interno')
def inicio_interno():
    
    nombres = session.get('nombres')
    apellidos = session.get('apellidos')

    if not nombres:
        nombres = 'Nombre de Usuario'

    if not apellidos:
        apellidos = 'Apellido de Usuario'

    datos = {
        'nombres': nombres,
        'apellidos': apellidos
    }

    return render_template('admin/inicio_interno.html', datos=datos)

@admin.route('/formularios_pendientes', methods=['GET'])
def formularios_pendientes():
    
    # Asegúrate de que 'nombres' y 'apellidos' estén definidos en la sesión
    nombres = session.get('nombres')
    apellidos = session.get('apellidos')

    if not nombres:
        nombres = 'Nombre de Usuario'

    if not apellidos:
        apellidos = 'Apellido de Usuario'

    datos = {
        'nombres': nombres,
        'apellidos': apellidos
    }
    
    page = request.args.get(get_page_parameter(), 1, type=int)
    conexion_MySQL = conectionBD()
    cursor = conexion_MySQL.cursor(dictionary=True)

    # Consulta para obtener el total de formularios
    sql_count = "SELECT COUNT(*) as total FROM datos WHERE estado = 'pendiente'"
    cursor.execute(sql_count)
    total_formularios = cursor.fetchone()['total']

    # Consulta para obtener los formularios paginados
    offset = (page - 1) * 10  # Asumiendo 10 formularios por página
    sql = "SELECT * FROM datos WHERE estado = 'pendiente' ORDER BY id ASC LIMIT %s, %s"
    cursor.execute(sql, (offset, 10))
    formularios = cursor.fetchall()

    pagination = Pagination(page=page, total=total_formularios, per_page=10, css_framework='bootstrap4')

    cursor.close()
    conexion_MySQL.close()

    # Pasa 'datos' a la plantilla
    return render_template('admin/formularios_pendientes.html', formularios=formularios, pagination=pagination, datos=datos) 


@admin.route('/formularios_aprobados', methods=['GET'])
def formularios_aprobados():
        
        page = request.args.get(get_page_parameter(), 1, type=int)
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        # Consulta para obtener el total de formularios aprobados
        sql_count = "SELECT COUNT(*) as total FROM datos WHERE estado = 'aprobado'"
        cursor.execute(sql_count)
        total_formularios = cursor.fetchone()['total']

        # Consulta para obtener los formularios aprobados paginados
        offset = (page - 1) * Paginas  # Paginas es la variable definida en tu código para el número de elementos por página
        sql = "SELECT * FROM datos WHERE estado = 'aprobado' ORDER BY id ASC LIMIT %s, %s"
        cursor.execute(sql, (offset, Paginas))
        formularios = cursor.fetchall()

        pagination = Pagination(page=page, total=total_formularios, per_page=Paginas, css_framework='bootstrap4')

 # Asegúrate de que 'nombres' y 'apellidos' estén definidos en la sesión
        nombres = session.get('nombres', 'Nombre de Usuario')
        apellidos = session.get('apellidos', 'Apellido de Usuario')

    # Define la variable 'datos' con los nombres y apellidos
        datos = {
        'nombres': nombres,
        'apellidos': apellidos
        }
        cursor.close()
        conexion_MySQL.close()
        return render_template('admin/formularios_aprobados.html', formularios=formularios, pagination=pagination, datos=datos)



@admin.route('/formularios_rechazados', methods=['GET'])
def formularios_rechazados():
    
        page = request.args.get(get_page_parameter(), 1, type=int)
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        # Consulta para obtener el total de formularios rechazados
        sql_count = "SELECT COUNT(*) as total FROM datos WHERE estado = 'rechazado'"
        cursor.execute(sql_count)
        total_formularios = cursor.fetchone()['total']

        # Consulta para obtener los formularios rechazados paginados
        offset = (page - 1) * Paginas  # Paginas es la variable definida en tu código para el número de elementos por página
        sql = "SELECT * FROM datos WHERE estado = 'rechazado' ORDER BY id ASC LIMIT %s, %s"
        cursor.execute(sql, (offset, Paginas))
        formularios = cursor.fetchall()

        pagination = Pagination(page=page, total=total_formularios, per_page=Paginas, css_framework='bootstrap4')

 # Asegúrate de que 'nombres' y 'apellidos' estén definidos en la sesión
        nombres = session.get('nombres', 'Nombre de Usuario')
        apellidos = session.get('apellidos', 'Apellido de Usuario')

    # Define la variable 'datos' con los nombres y apellidos
        datos = {
        'nombres': nombres,
        'apellidos': apellidos
        }
        cursor.close()
        conexion_MySQL.close()

        return render_template('admin/formularios_rechazados.html', formularios=formularios, pagination=pagination, datos=datos)

@admin.route('/formularios_todos', methods=['GET', 'POST'])
def formularios_todos():
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        page = request.args.get(get_page_parameter(), 1, type=int)

        # Convertir las fechas a objetos datetime.date si están presentes
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except ValueError:
                fecha_inicio = None  # Fecha de inicio no válida
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                fecha_fin = None  # Fecha de fin no válida

        # Lógica para filtrar los formularios por el rango de fechas
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        try:
            # Consulta base para obtener los formularios
            sql = "SELECT * FROM datos WHERE 1=1"
            params = ()

            # Agregar condiciones de filtrado por fechas si están presentes
            if fecha_inicio:
                sql += " AND fecha_recepcion >= %s"
                params += (fecha_inicio,)
            if fecha_fin:
                sql += " AND fecha_recepcion <= %s"
                params += (fecha_fin,)

            # Consultar el total de formularios que cumplen con los criterios de filtro
            cursor.execute(sql, params)
            total_formularios = cursor.rowcount

            # Aplicar paginación a la consulta
            offset = (page - 1) * Paginas  # Asumiendo 10 formularios por página
            sql += " ORDER BY id ASC LIMIT %s, %s"
            params += (offset, Paginas)

            # Ejecutar la consulta para obtener los formularios paginados
            cursor.execute(sql, params)
            formularios = cursor.fetchall()

            pagination = Pagination(page=page, total=total_formularios, per_page=Paginas, css_framework='bootstrap4')

            # Asegúrate de que 'nombres' y 'apellidos' estén definidos en la sesión
            nombres = session.get('nombres', 'Nombre de Usuario')
            apellidos = session.get('apellidos', 'Apellido de Usuario')

            # Define la variable 'datos' con los nombres y apellidos
            datos = {
                'nombres': nombres,
                'apellidos': apellidos
            }

            # Pasa 'datos' a la plantilla
            return render_template('admin/formularios_todos.html', formularios=formularios, pagination=pagination, datos=datos)
        finally:
            # Asegurarse de que todos los resultados se lean o descarten antes de cerrar el cursor
            cursor.fetchall()  # Esto lee todos los resultados
            cursor.close()
            conexion_MySQL.close()
            
    else:  # Método GET
        page = request.args.get(get_page_parameter(), 1, type=int)

        # Lógica para obtener todos los formularios sin filtrar
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        try:
            # Consulta para obtener el total de formularios
            sql_count = "SELECT COUNT(*) as total FROM datos"
            cursor.execute(sql_count)
            total_formularios = cursor.fetchone()['total']

            # Consulta para obtener los formularios paginados
            offset = (page - 1) * Paginas  # Asumiendo 10 formularios por página
            sql = "SELECT * FROM datos ORDER BY id ASC LIMIT %s, %s"
            cursor.execute(sql, (offset, Paginas))
            formularios = cursor.fetchall()

            pagination = Pagination(page=page, total=total_formularios, per_page=Paginas, css_framework='bootstrap4')

            # Asegúrate de que 'nombres' y 'apellidos' estén definidos en la sesión
            nombres = session.get('nombres', 'Nombre de Usuario')
            apellidos = session.get('apellidos', 'Apellido de Usuario')

            # Define la variable 'datos' con los nombres y apellidos
            datos = {
                'nombres': nombres,
                'apellidos': apellidos
            }

            # Pasa 'datos' a la plantilla
            return render_template('admin/formularios_todos.html', formularios=formularios, pagination=pagination, datos=datos)
        finally:
            # Cerrar el cursor y la conexión en un bloque finally para asegurar que se cierren incluso si ocurre una excepción
            cursor.close()
            conexion_MySQL.close()


@admin.route('/confirmar_datos', methods=['GET', 'POST'])
def confirmar_datos():
        if request.method == 'POST':
            # Obtener los datos del formulario de confirmación
            datos_confirmados = {
                'nombres': request.form['nombres'],
                'apellidos': request.form['apellidos'],
                'cedula': request.form['cedula'],
                'fnacimiento': request.form['fnacimiento']
            }

            # Verificar si los datos coinciden con los de la sesión
            if datos_confirmados == session['datos_formulario']:
                print(f"Datos confirmados: {datos_confirmados}")

                # Guardar los datos en la base de datos
                try:
                    conexion_MySQL = conectionBD()
                    with conexion_MySQL.cursor(dictionary=True) as cursor:
                        sql = "INSERT INTO datos (cedula, nombres, apellidos, fnacimiento, correo, correo2, fecha_registro,fecha_recepcion) VALUES (%s, %s, %s, %s, %s, %s, NOW(),NOW())"
                        valores = (datos_confirmados['cedula'], datos_confirmados['nombres'], datos_confirmados['apellidos'], datos_confirmados['fnacimiento'], session['datos_formulario']['correo'], session['datos_formulario']['correo2'])
                        cursor.execute(sql, valores)
                        conexion_MySQL.commit()
                except conexion_MySQL.connector.Error as err:
                    print(f"Error al guardar los datos en la base de datos: {err}")
                finally:
                    if conexion_MySQL.is_connected():
                        conexion_MySQL.close()

            return render_template('admin/datos_confirmar.html', datos=session['datos_formulario'])

@admin.route('/admin/formularios_pendientes/<int:id>', methods=['POST'])
def procesar_formulario(id):
        # Determina si el formulario fue aprobado o rechazado
        accion = request.form.get('accion')

        # Actualiza el estado del formulario en la base de datos
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)
        password_temporal = None # Initialize password_temporal outside the if block
        cuerpo = "" # Initialize cuerpo outside the if block
        if accion == 'aprobar':
            # Genera una contraseña temporal
            password_temporal = secrets.token_urlsafe(16)
            
            # Actualiza el estado y la contraseña temporal en la base de datos
            sql = "UPDATE datos SET estado = 'aprobado', password_temporal = %s WHERE id = %s"
            cursor.execute(sql, (password_temporal, id))
            conexion_MySQL.commit()

            # Recupera el correo electrónico del destinatario
            sql_correo = "SELECT correo FROM datos WHERE id = %s"
            cursor.execute(sql_correo, (id,))
            destinatario = cursor.fetchone()
            if destinatario:
                destinatario = destinatario['correo']
            else:
                # Manejar el caso en que no se encuentre el destinatario
                return "No se encontró el destinatario", 404

            # Prepara el correo electrónico con la contraseña temporal
            asunto = "Suscripción Aprobada"
            cuerpo = f"¡Bienvenido/a a Copaco S.A!. Tu contraseña temporal es: {password_temporal}"
        else:
            # Para el caso de rechazo, solo actualiza el estado
            sql = "UPDATE datos SET estado = 'rechazado' WHERE id = %s"
            cursor.execute(sql, (id,))
            conexion_MySQL.commit()

            # No necesitas enviar un correo para el caso de rechazo
            return redirect(url_for('admin.formularios_pendientes'))

        cursor.close()
        conexion_MySQL.close()

        # Envía el correo electrónico utilizando la función personalizada
        if password_temporal: # Check if password_temporal is not None before calling enviar_correo
            enviar_correo(destinatario, cuerpo, password_temporal)

        # Redirige al usuario a la página deseada
        return redirect(url_for('admin.formularios_pendientes'))
    

    
def obterner_formularios(offset=0):
        conexion_MySQL = conectionBD()  # Se conecta a la base de datos
        cursor = conexion_MySQL.cursor(dictionary=True)  # Crea un cursor para ejecutar consultas

        # Consulta para obtener el total de formularios pendientes
        sql_count = "SELECT COUNT(*) as total FROM datos WHERE estado = 'pendiente'"
        cursor.execute(sql_count)
        total_formularios = cursor.fetchone()['total']  # Obtiene el total de formularios

        per_page = 10  # Número de formularios por página
        # Consulta para obtener los formularios pendientes paginados
        sql = "SELECT * FROM datos WHERE estado = 'pendiente' ORDER BY id ASC LIMIT %s, %s"
        cursor.execute(sql, (offset, per_page))
        formularios = cursor.fetchall()  # Obtiene los formularios paginados

        cursor.close()  # Cierra el cursor
        conexion_MySQL.close()  # Cierra la conexión a la base de datos

        return formularios, total_formularios  # Retorna los formularios y el total de formularios

'''
@admin.route('admin/imagenes')
def admin_imagenes():
    imagenes=Imagen.query.all()
    return render_template('admin/formularios_pendientes.html', imagenes=imagenes)

@admin.route('/admin/imagen/path:filename')
def imagen_usuario(filename):
    return send_from_directory(miapp.config['UPLOAD_FOLDER'], filename)'''

def register_admin_blueprint(app):
        app.register_blueprint(admin, url_prefix='/admin')
       
        
@admin.route('/cerrar_sesion')
def cerrar_sesion():
        # Elimina cualquier información de sesión relacionada con el usuario
        session.clear()

        # Redirige al usuario a la página de inicio de sesión o a otra página deseada
        return redirect(url_for('login')) 
    
'''@admin.route('/inicio_interno')
def admin_inicio_interno():
        
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        # Recuperar todos los formularios
        sql = "SELECT * FROM datos"
        cursor.execute(sql)
        todos_formularios = cursor.fetchall()

        # Filtrar por estado
        formularios_pendientes = [f for f in todos_formularios if f['estado'] == 'pendiente']
        formularios_aprobados = [f for f in todos_formularios if f['estado'] == 'aprobado']
        formularios_rechazados = [f for f in todos_formularios if f['estado'] == 'rechazado']

        cursor.close()
        conexion_MySQL.close()

        # Pasar los formularios filtrados a la plantilla
        return render_template('admin/inicio_interno.html', formularios_pendientes=formularios_pendientes, formularios_aprobados=formularios_aprobados, formularios_rechazados=formularios_rechazados, datos={'nombres': 'Nombre de Usuario', 'apellidos': 'Apellido de Usuario'})
'''
        
'''@admin.route('/formularios')
    def formularios():
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor(dictionary=True)

            # Recuperar todos los formularios
            sql = "SELECT * FROM datos"
            cursor.execute(sql)
            formularios = cursor.fetchall()

            cursor.close()
            conexion_MySQL.close()
            return render_template('admin/formularios.html')'''

'''@admin.route('/listar_aprobados', methods=['GET'])
    def listar_aprobados():
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        # Recuperar todos los formularios aprobados
        sql = "SELECT * FROM datos WHERE estado = 'aprobado'"
        cursor.execute(sql)
        formularios_aprobados = cursor.fetchall()

        cursor.close()
        conexion_MySQL.close()
        return render_template('admin/formularios_aprobados.html', formularios=formularios_aprobados)'''
'''@admin.route('/listar_pendientes', methods=['GET'])
    def listar_pendientes():
        conexion_MySQL = conectionBD()
        cursor = conexion_MySQL.cursor(dictionary=True)

        # Recuperar todos los formularios pendientes
        sql = "SELECT * FROM datos WHERE estado = 'pendiente'"
        cursor.execute(sql)
        formularios_pendientes = cursor.fetchall()

        cursor.close()
        conexion_MySQL.close()
        return render_template('admin/formularios_pendientes.html', formularios=formularios_pendientes)'''



"""@interno.route('/recibir-formulario', methods=['GET', 'POST'])
    def recibir_formulario():
            if request.method == 'POST':
                print(request.form)
                if 'nombres' in request.form and 'apellidos' in request.form and 'cedula' in request.form and 'fnacimiento' in request.form:
                    nombres_confirmados = request.form['nombres']
                    apellidos_confirmados = request.form['apellidos']
                    cedula_confirmada = request.form['cedula']
                    fnacimiento_confirmado = request.form['fnacimiento']
                    # Procesar los datos
                    conexion_MySQL = conectionBD()
                    cursor = conexion_MySQL.cursor()

                    sql = "INSERT INTO datos (cedula, nombres, apellidos, fnacimiento) VALUES (%s, %s, %s, %s)"
                    valores = (cedula_confirmada, nombres_confirmados, apellidos_confirmados, fnacimiento_confirmado)
                    cursor.execute(sql, valores)
                    conexion_MySQL.commit()

                    cursor.close()
                    conexion_MySQL.close()

                    return redirect(url_for('interno.formularios'))
                else:
                    # Manejar el caso en que los campos esperados no estén presentes
                    print("Faltan campos en el formulario.")
                    return redirect(url_for('interno.inicio_interno'))
            else:
                return render_template('formulario.html')
    """

"""@interno.route('/interno/formularios', methods=['GET'])
    def formularios():
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor(dictionary=True)

            # Recuperar todos los formularios
            sql = "SELECT * FROM datos"
            cursor.execute(sql)
            formularios = cursor.fetchall()

            cursor.close()
            conexion_MySQL.close()

            return render_template('interno/formularios.html', formularios=formularios)
    """

"""
    @interno.route('/interno/formularios_pendientes', methods=['GET'])
    def formularios_pendientes():
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor(dictionary=True)

            # Asumiendo que tienes una columna 'estado' en tu tabla 'datos' que indica si el formulario está pendiente
            sql = "SELECT * FROM datos WHERE estado = 'pendiente'"
            cursor.execute(sql)
            formularios = cursor.fetchall()

            cursor.close()
            conexion_MySQL.close()

            return redirect(url_for('interno/formulario_pendientes.html', formularios=formularios))
    """
"""
    @interno.route('/interno/aprobar_formulario/<int:id>', methods=['POST'])
    def aprobar_formulario(id):
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor()

            sql = "UPDATE datos SET estado = 'aprobado' WHERE id = %s"
            cursor.execute(sql, (id,))
            conexion_MySQL.commit()

            cursor.close()
            conexion_MySQL.close()

            return redirect(url_for('interno.formularios'))
    """
"""
    @interno.route('/interno/rechazar_formulario/<int:id>', methods=['POST'])
    def rechazar_formulario(id):
            conexion_MySQL = conectionBD()
            cursor = conexion_MySQL.cursor()

            sql = "UPDATE datos SET estado = 'rechazado' WHERE id = %s"
            cursor.execute(sql, (id,))
            conexion_MySQL.commit()

            cursor.close()
            conexion_MySQL.close()

            return redirect(url_for('interno.formularios'))
    """
"""
    @interno.route('/interno/confirmar_datos', methods=['GET', 'POST'])
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

                    # Corrección aquí: Usa el nombre del blueprint y la función de vista
                    return redirect(url_for('interno.formularios'))
                else:
                    msg = 'La información en el formulario no coincide con los datos confirmados'
                    return render_template('interno/formularios.html', msg=msg)
            else:
                return render_template('interno/formularios.html', datos=session['datos_formulario'])
            
    """     
"""
    @interno.route('/')
    def home():
            return render_template('externo/login.html')

    def conectionBD():
            import mysql.connector
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="registro"   
            )
            return conexion
    """