from flask import request, jsonify, send_file
# from . import db
# from models.usuario import Usuario
# from models.rol import Rol
from werkzeug.utils import secure_filename  # Para asegurar los nombres de archivo
# from resources.Autenticacion import TokenGenerator
# Importación de funciones para subir imagenes
from utils.update_files import allowed_file_img, allowed_file, stringAleatorio
import os  # Para acceder a variables de entorno y operaciones del sistema
from utils.optimize_image import optimize_image  # Para optimizar imágenes

def f_upload_file_foto_perfil():
    if 'files[]' not in request.files:
        return jsonify({"message": 'No hay imagenes en la solicitud', "status": 'failed'}), 400

    files = request.files.getlist('files[]')
    errors = []
    success = False

    for file in files:
        if file and allowed_file_img(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'files_fotoperfil')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            upload_path = os.path.join(upload_directory, filename)
            
            try:
                optimize_image(file, upload_path) # Guardar la imagen usando optimización
                success = True
            except Exception as e:
                errors.append({'filename': file.filename, 'message': str(e)})

        else:
            errors.append({'filename': file.filename, 'message': 'Tipo de archivo no permitido.'})

    if success:
        if errors:
            status_code = 207  # Código de estado HTTP para respuesta parcial
            message = 'Algunos archivos no se pudieron subir correctamente.'
        else:
            status_code = 201
            message = 'Todos los archivos subidos correctamente.'
    else:
        status_code = 400
        message = 'Ningún archivo subido correctamente.'

    return jsonify({"message": message, "errors": errors, "status": 'success' if success else 'failed'}), status_code



def f_upload_file_pago():
    if 'files[]' not in request.files:
        return jsonify({"message": 'No hay archivos en la solicitud', "status": 'failed'}), 400
    
    files = request.files.getlist('files[]')
    errors = []
    success = False
    
    for file in files:
        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'files_pago')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            # nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, filename)

            file.save(upload_path)
            success = True
        else:
            errors.append({'filename': file.filename, 'message': 'Tipo de archivo no permitido.'})

    if success:
        if errors:
            status_code = 207  # Código de estado HTTP para respuesta parcial
            message = 'Algunos archivos no se pudieron subir.'
        else:
            status_code = 201
            message = 'Todos los archivos subidos correctamente.'
    else:
        status_code = 400
        message = 'Ningún archivo subido correctamente.'

    return jsonify({"message": message, "errors": errors, "status": 'success' if success else 'failed'}), status_code


def f_upload_file_texto():
    if 'files[]' not in request.files:
        return jsonify({"message": 'No hay archivos en la solicitud', "status": 'failed'}), 400
    
    files = request.files.getlist('files[]')
    errors = []
    success = False
    
    for file in files:
        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'files_texto')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            # nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, filename)

            file.save(upload_path)
            success = True
        else:
            errors.append({'filename': file.filename, 'message': 'Tipo de archivo no permitido.'})

    if success:
        if errors:
            status_code = 207  # Código de estado HTTP para respuesta parcial
            message = 'Algunos archivos no se pudieron subir.'
        else:
            status_code = 201
            message = 'Todos los archivos subidos correctamente.'
    else:
        status_code = 400
        message = 'Ningún archivo subido correctamente.'

    return jsonify({"message": message, "errors": errors, "status": 'success' if success else 'failed'}), status_code


def f_registrarArchivo():
    try:
        if 'archivo' not in request.files:
            raise ValueError("No se proporcionó ningún archivo en la solicitud.")

        file = request.files['archivo']

        if file.filename == '':
            raise ValueError("Nombre de archivo vacío.")

        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            upload_directory = os.path.join(basepath, 'static', 'archivos')

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            filename = secure_filename(file.filename)
            nuevo_nombre_file = stringAleatorio() + os.path.splitext(filename)[1]
            upload_path = os.path.join(upload_directory, nuevo_nombre_file)

            file.save(upload_path)

            resp = {
                "status": "success",
                "message": "Archivo subido correctamente",
                "filename": nuevo_nombre_file  # Puedes enviar el nuevo nombre del archivo si es necesario
            }
            return jsonify(resp), 200
        else:
            raise ValueError("Tipo de archivo no permitido.")

    except Exception as e:
        resp = {
            "status": "error",
            "message": f"Error al subir el archivo: {str(e)}"
        }
        return jsonify(resp), 500
    

def f_download_file(file_name):
    archivo_path = 'static/files_pago/' + file_name
    return send_file(archivo_path, as_attachment=True)


def f_download_file_texto(file_name):
    archivo_path = 'static/files_texto/' + file_name
    return send_file(archivo_path, as_attachment=True)

def f_listarArchivos():
    basepath = os.path.dirname(__file__)
    upload_directory = os.path.join(basepath, 'static', 'archivos')

    if not os.path.exists(upload_directory):
        return jsonify({"archivos": []})

    archivos = os.listdir(upload_directory)
    return jsonify({"archivos": archivos})

def f_eliminarArchivo(filename):
    try:
        basepath = os.path.dirname(__file__)
        upload_directory = os.path.join(basepath, 'static', 'archivos')

        file_path = os.path.join(upload_directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            resp = {
                "status": "success",
                "message": f"Archivo {filename} eliminado correctamente"
            }
            return jsonify(resp), 200
        else:
            raise FileNotFoundError(f"El archivo {filename} no existe.")

    except Exception as e:
        resp = {
            "status": "error",
            "message": f"Error al eliminar el archivo: {str(e)}"
        }
        return jsonify(resp), 500