#C:\xampp\miapp\usuario\forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from werkzeug.utils import secure_filename
import os
import re
from dateutil.relativedelta import relativedelta
import datetime


class RegistroForm(FlaskForm):
    cedula = StringField('Cedula', validators=[Length(max=10, min=6, message="La cédula debe tener como minimo 6 digitos.")])
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=20)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=20)])
    fnacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired(message="La fecha de nacimiento es obligatoria.")])
    telefono = StringField('Telefono', validators=[DataRequired(), Length(max=10)])
    correo = StringField('Correo', validators=[DataRequired(), Email(message="Correo no válido. Por favor, introduce un correo electrónico válido.")])
    correo2 = StringField('Confirmar Correo', validators=[DataRequired(), EqualTo('correo', message="Los correos no coinciden. Por favor, introduce el mismo correo.")])
    cedula_adelante = FileField('Foto de tú CI - Adelante', validators=[DataRequired()])
    cedula_atras = FileField('Foto de tú CI - Atras', validators=[DataRequired()])
    selfie = FileField('Una Selfie', validators=[DataRequired()])
    
    submit = SubmitField('Registrar')

    def validate_cedula(self, cedula):
        if not cedula.data.isdigit():
            raise ValidationError('Nro de Cedula debe ser solo numeros.')

    def validate_nombres(self, nombres):
        if not re.match(r"^[a-zA-Z\s]*$", nombres.data):
            raise ValidationError('Solo se permiten letras y espacios.')

    def validate_apellidos(self, apellidos):
        if not re.match(r"^[a-zA-Z\s]*$", apellidos.data):
            raise ValidationError('Solo se permiten letras y espacios.')
    
    def validate_fnacimiento(self, fnacimiento):
        edad = relativedelta(datetime.date.today(), fnacimiento.data)
        if edad.years < 18:
            raise ValidationError('Debes ser mayor de 18 años para registrarte.')

    def validate_telefono(self, telefono):
        if not telefono.data.isdigit():
            raise ValidationError('Telefono debe ser solo numeros.')

    def validate_cedula_adelante(self, cedula_adelante):
        if cedula_adelante.data and not self.is_image(cedula_adelante.data):
            raise ValidationError('Tú CI debe ser una imagen.')
        if cedula_adelante.data and self.is_file_too_large(cedula_adelante.data):
            raise ValidationError('Tú CI es demasiado grande.')

    def validate_cedula_atras(self, cedula_atras):
        if cedula_atras.data and not self.is_image(cedula_atras.data):
            raise ValidationError('Tú CI debe ser una imagen.')
        if cedula_atras.data and self.is_file_too_large(cedula_atras.data):
            raise ValidationError('Tú CI es demasiado grande.')

    def validate_selfie(self, selfie):
        if selfie.data and not self.is_image(selfie.data):
            raise ValidationError('Selfie debe ser una imagen.')
        if selfie.data and self.is_file_too_large(selfie.data):
            raise ValidationError('Selfie es demasiado grande.')
        

    def is_image(self, file):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def is_file_too_large(self, file):
        MAX_FILE_SIZE = 8 * 1024 * 1024 # 8MB
        return file.content_length > MAX_FILE_SIZE

