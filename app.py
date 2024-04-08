# app.py

from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file


app = Flask(__name__)
app.register_blueprint(interno)

app.secret_key = 'tu_clave_secreta'

# Configuración de CORS
CORS(app)

# Registro de los blueprints
from externo import externo
from interno import interno
app.register_blueprint(externo)
app.register_blueprint(interno)

# El resto de tu código de configuración aquí

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
