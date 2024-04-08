# config.py

general_folder_path = r'C:\xampp\login\imagensubida'
UPLOAD_FOLDER = general_folder_path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS