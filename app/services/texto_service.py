from flask import jsonify, make_response
from http import HTTPStatus

from core.database import db
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError

from models.texto_model import Texto, db
from models.texto_model import MateriaTexto, TipoExtensionTexto, Texto, TipoIdiomaTexto, TipoCategoriaTexto, db
from models.materia_model import Materia
from models.inscripcion_model import Inscripcion
from models.curso_materia_model import CursoMateria

import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def getListTexto():
    try:
        textos = Texto.query.order_by(Texto.texnombre).all()
        response = [texto.to_dict() for texto in textos]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createTexto(data, request):
    try:
        # Guardar el archivo de request
        archivo_nombre = saveFileTexto(request)

        static_dir = os.getenv('STATIC_DIR', 'static')
        files_textos_dir = os.getenv('FILES_TEXTOS_DIR', 'files_textos')

        # Crear un nuevo registro de texto
        nuevo_texto = Texto(
            texnombre=data['texnombre'],
            textipo=data.get('textipo'),
            texformato=data.get('texformato'),
            texdocumento=archivo_nombre,
            texruta='/' + static_dir + '/' + files_textos_dir + '/' + archivo_nombre,
            texdescripcion=data.get('texdescripcion'),
            texautor=data.get('texautor'),
            texsize=data.get('texsize'),
            texextension=data.get('texextension'),
            texidioma=data.get('texidioma'),
            texfecpublicacion=data.get('texfecpublicacion'),
            texcategoria=data.get('texcategoria'),
            texusureg=data.get('texusureg'),
            texusumod=data.get('texusureg'),
            texfecmod=datetime.now(),
            texestado=data.get('texestado', 1)
        )
        db.session.add(nuevo_texto)
        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El texto fue creado correctamente.",
            "texto": nuevo_texto.to_dict()  # Devuelve los detalles del nuevo texto
        }
        return make_response(jsonify(resp), HTTPStatus.CREATED)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al crear el texto: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)


def updateTexto(data, textid, request):
    try:
        # Guardar el archivo nuevo (si se proporciona uno)
        archivo_nombre = saveFileTexto(request)

        # Obtener las rutas desde las variables de entorno
        static_dir = os.getenv('STATIC_DIR', 'static')
        files_textos_dir = os.getenv('FILES_TEXTOS_DIR', 'files_textos')

        # Obtener el registro de texto existente
        texto = Texto.query.get(textid)
        if not texto:
            raise ValueError(f"No se encontró el texto con ID {textid}.")

        # Eliminar el archivo anterior si se ha subido uno nuevo
        if archivo_nombre and texto.texruta:
            old_file_path = os.path.join(os.path.dirname(
                __file__), '..', static_dir, files_textos_dir, texto.texruta)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        # Actualizar los campos del texto
        texto.texnombre = data.get('texnombre', texto.texnombre)
        texto.textipo = data.get('textipo', texto.textipo)
        texto.texformato = data.get('texformato', texto.texformato)
        if archivo_nombre:
            texto.texruta = '/' + static_dir + '/' + \
                files_textos_dir + '/' + archivo_nombre,
            texto.texdocumento = archivo_nombre
            texto.texsize = data.get('texsize', texto.texsize)
        texto.texdescripcion = data.get('texdescripcion', texto.texdescripcion)
        texto.texautor = data.get('texautor', texto.texautor)
        texto.texextension = data.get('texextension', texto.texextension)
        texto.texidioma = data.get('texidioma', texto.texidioma)
        texto.texfecpublicacion = data.get(
            'texfecpublicacion', texto.texfecpublicacion)
        texto.texcategoria = data.get('texcategoria', texto.texcategoria)
        texto.texusumod = data['texusumod']
        texto.texfecmod = datetime.now()
        texto.texestado = data.get('texestado', texto.texestado)

        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El texto fue modificado correctamente.",
            "texto": texto.to_dict(),
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al modificar el texto: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteTexto(textid):
    try:
        # Obtener las rutas desde las variables de entorno
        static_dir = os.getenv('STATIC_DIR', 'static')
        files_textos_dir = os.getenv('FILES_TEXTOS_DIR', 'files_textos')

        # Obtener el registro de texto existente
        texto = Texto.query.get(textid)
        if not texto:
            raise ValueError(f"No se encontró el texto con ID {textid}.")

        # Eliminar el archivo asociado si existe
        if texto.texdocumento:
            file_path = os.path.join(os.path.dirname(
                __file__), '..', static_dir, files_textos_dir, texto.texdocumento)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Eliminar el registro de la base de datos
        db.session.delete(texto)
        db.session.commit()

        # Respuesta exitosa
        resp = {
            "status": "success",
            "message": "El texto y su archivo asociado fueron eliminados correctamente."
        }
        return make_response(jsonify(resp), HTTPStatus.OK)

    except Exception as e:
        db.session.rollback()
        resp = {
            "status": "error",
            "message": f"Error al eliminar el texto: {str(e)}"
        }
        return make_response(jsonify(resp), HTTPStatus.INTERNAL_SERVER_ERROR)


def getListTipoExtensionTexto():
    try:
        tipo_extension_textos = TipoExtensionTexto.query.order_by(
            TipoExtensionTexto.tipextnombre).all()
        response = [tipo_extension_texto.to_dict()
                    for tipo_extension_texto in tipo_extension_textos]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createTipoExtensionTexto(data):
    try:
        tipo_extension_texto = TipoExtensionTexto(
            tipextnombre=data["tipextnombre"]
        )
        db.session.add(tipo_extension_texto)
        db.session.commit()
        _data = tipo_extension_texto.to_dict()
        response_data = {
            "message": "TipoExtensionTexto created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        return make_response(jsonify(response_data), HTTPStatus.CREATED)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def updateTipoExtensionTexto(data, tipextid):
    try:
        tipo_extension_texto = TipoExtensionTexto.query.get(tipextid)
        if tipo_extension_texto is None:
            return make_response(jsonify({"error": "TipoExtensionTexto not found."}), HTTPStatus.NOT_FOUND)

        tipo_extension_texto.tipextnombre = data["tipextnombre"]
        db.session.commit()
        _data = tipo_extension_texto.to_dict()
        response_data = {
            "message": "TipoExtensionTexto updated successfully.",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteTipoExtensionTexto(tipextid):
    try:
        tipo_extension_texto = TipoExtensionTexto.query.get(tipextid)
        if tipo_extension_texto is None:
            return make_response(jsonify({"error": "TipoExtensionTexto not found."}), HTTPStatus.NOT_FOUND)
        db.session.delete(tipo_extension_texto)
        db.session.commit()
        return make_response(jsonify({"message": "TipoExtensionTexto deleted successfully."}), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getListTipoCategoriaTexto():
    try:
        tipo_categoria_textos = TipoCategoriaTexto.query.order_by(
            TipoCategoriaTexto.tipcatnombre).all()
        response = [tipo_categoria_texto.to_dict()
                    for tipo_categoria_texto in tipo_categoria_textos]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createTipoCategoriaTexto(data):
    try:
        tipo_categoria_texto = TipoCategoriaTexto(
            tipcatnombre=data["tipcatnombre"]
        )
        db.session.add(tipo_categoria_texto)
        db.session.commit()
        _data = tipo_categoria_texto.to_dict()
        response_data = {
            "message": "TipoCategoriaTexto created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        return make_response(jsonify(response_data), HTTPStatus.CREATED)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def updateTipoCategoriaTexto(data, tipcatid):
    try:
        tipo_categoria_texto = TipoCategoriaTexto.query.get(tipcatid)
        if tipo_categoria_texto is None:
            return make_response(jsonify({"error": "TipoCategoriaTexto not found."}), HTTPStatus.NOT_FOUND)

        tipo_categoria_texto.tipcatnombre = data["tipcatnombre"]
        db.session.commit()
        _data = tipo_categoria_texto.to_dict()
        response_data = {
            "message": "TipoCategoriaTexto updated successfully.",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteTipoCategoriaTexto(tipcatid):
    try:
        tipo_categoria_texto = TipoCategoriaTexto.query.get(tipcatid)
        if tipo_categoria_texto is None:
            return make_response(jsonify({"error": "TipoCategoriaTexto not found."}), HTTPStatus.NOT_FOUND)
        db.session.delete(tipo_categoria_texto)
        db.session.commit()
        return make_response(jsonify({"message": "TipoCategoriaTexto deleted successfully."}), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getListTipoIdiomaTexto():
    try:
        tipo_idioma_textos = TipoIdiomaTexto.query.order_by(
            TipoIdiomaTexto.tipidinombre).all()
        response = [tipo_idioma_texto.to_dict()
                    for tipo_idioma_texto in tipo_idioma_textos]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createTipoIdiomaTexto(data):
    try:
        tipo_idioma_texto = TipoIdiomaTexto(
            tipidinombre=data["tipidinombre"]
        )
        db.session.add(tipo_idioma_texto)
        db.session.commit()
        _data = tipo_idioma_texto.to_dict()
        response_data = {
            "message": "TipoIdiomaTexto created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        return make_response(jsonify(response_data), HTTPStatus.CREATED)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def updateTipoIdiomaTexto(data, tipidiid):
    try:
        tipo_idioma_texto = TipoIdiomaTexto.query.get(tipidiid)
        if tipo_idioma_texto is None:
            return make_response(jsonify({"error": "TipoIdiomaTexto not found."}), HTTPStatus.NOT_FOUND)

        tipo_idioma_texto.tipidinombre = data["tipidinombre"]
        db.session.commit()
        _data = tipo_idioma_texto.to_dict()
        response_data = {
            "message": "TipoIdiomaTexto updated successfully.",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteTipoIdiomaTexto(tipidiid):
    try:
        tipo_idioma_texto = TipoIdiomaTexto.query.get(tipidiid)
        if tipo_idioma_texto is None:
            return make_response(jsonify({"error": "TipoIdiomaTexto not found."}), HTTPStatus.NOT_FOUND)
        db.session.delete(tipo_idioma_texto)
        db.session.commit()
        return make_response(jsonify({"message": "TipoIdiomaTexto deleted successfully."}), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getListTipoTexto():
    try:
        tipo_textos = TipoTexto.query.order_by(TipoTexto.tiptexnombre).all()
        response = [tipo_texto.to_dict() for tipo_texto in tipo_textos]
        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createTipoTexto(data):
    try:
        tipo_texto = TipoTexto(
            tiptexnombre=data["tiptexnombre"]
        )
        db.session.add(tipo_texto)
        db.session.commit()
        _data = tipo_texto.to_dict()
        response_data = {
            "message": "TipoTexto created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        return make_response(jsonify(response_data), HTTPStatus.CREATED)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def updateTipoTexto(data, tiptexid):
    try:
        tipo_texto = TipoTexto.query.get(tiptexid)
        if tipo_texto is None:
            return make_response(jsonify({"error": "TipoTexto not found."}), HTTPStatus.NOT_FOUND)

        tipo_texto.tiptexnombre = data["tiptexnombre"]
        db.session.commit()
        _data = tipo_texto.to_dict()
        response_data = {
            "message": "TipoTexto updated successfully.",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteTipoTexto(tiptexid):
    try:
        tipo_texto = TipoTexto.query.get(tiptexid)
        if tipo_texto is None:
            return make_response(jsonify({"error": "TipoTexto not found."}), HTTPStatus.NOT_FOUND)
        db.session.delete(tipo_texto)
        db.session.commit()
        return make_response(jsonify({"message": "TipoTexto deleted successfully."}), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getListMateriaTexto():
    try:
        # Crear alias para las tablas con aliased
        M = aliased(Materia)
        T = aliased(Texto)

        # Realizar la consulta con los joins necesarios
        query = (db.session.query(
            MateriaTexto.mattexid, MateriaTexto.matid, MateriaTexto.texid, MateriaTexto.mattexdescripcion,
            MateriaTexto.mattexusureg, MateriaTexto.mattexfecreg, MateriaTexto.mattexusumod,
            MateriaTexto.mattexfecmod, MateriaTexto.mattexestado, M.matnombre, M.matnivel, M.matdesnivel,
            T.texnombre, T.texdocumento
        )
            .join(M, M.matid == MateriaTexto.matid)
            .join(T, T.texid == MateriaTexto.texid)
            .order_by(M.matnombre, T.texnombre)
            .distinct()
            .all()
        )

        # Asignamos el resultado a una lista
        materia_textos = query
        # Formatear los datos en response
        response = []

        for row in materia_textos:
            materia_texto_dict = {
                'mattexid': row.mattexid,
                'matid': row.matid,
                'matnombre': row.matnombre,
                'matnivel': row.matnivel,
                'matdesnivel': row.matdesnivel,
                'texid': row.texid,
                'texnombre': row.texnombre,
                'texdocumento': row.texdocumento,
                'mattexdescripcion': row.mattexdescripcion,
                'mattexusureg': row.mattexusureg,
                'mattexfecreg': row.mattexfecreg.isoformat() if row.mattexfecreg else None,
                'mattexusumod': row.mattexusumod,
                'mattexfecmod': row.mattexfecmod.isoformat() if row.mattexfecmod else None,
                'mattexestado': row.mattexestado,
                'matnombre': row.matnombre,
                'matnivel': row.matnivel,
                'texnombre': row.texnombre
            }
            response.append(materia_texto_dict)

        return make_response(jsonify(response), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def createMateriaTexto(data):
    try:
        materia_texto = MateriaTexto(
            matid=data["matid"],
            texid=data["texid"],
            mattexdescripcion=data.get("mattexdescripcion"),
            mattexusureg=data.get("mattexusureg"),
            mattexfecreg=datetime.now(),
            mattexusumod=data.get("mattexusureg"),
            mattexfecmod=datetime.now(),
            mattexestado=data.get("mattexestado", 1)
        )
        db.session.add(materia_texto)
        db.session.commit()
        _data = materia_texto.to_dict()
        response_data = {
            "message": "MateriaTexto created successfully",
            "data": _data,
            "code": HTTPStatus.CREATED
        }
        return make_response(jsonify(response_data), HTTPStatus.CREATED)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def updateMateriaTexto(data, mattexid):
    try:
        materia_texto = MateriaTexto.query.get(mattexid)
        if materia_texto is None:
            return make_response(jsonify({"error": "MateriaTexto not found."}), HTTPStatus.NOT_FOUND)

        materia_texto.matid = data.get("matid", materia_texto.matid)
        materia_texto.texid = data.get("texid", materia_texto.texid)
        materia_texto.mattexdescripcion = data.get(
            "mattexdescripcion", materia_texto.mattexdescripcion)
        materia_texto.mattexusumod = data.get(
            "mattexusumod", materia_texto.mattexusumod)
        materia_texto.mattexfecmod = datetime.now()
        materia_texto.mattexestado = data.get(
            "mattexestado", materia_texto.mattexestado)

        db.session.commit()
        _data = materia_texto.to_dict()
        response_data = {
            "message": "MateriaTexto updated successfully.",
            "data": _data,
            "code": HTTPStatus.OK
        }
        return make_response(jsonify(response_data), HTTPStatus.OK)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def deleteMateriaTexto(mattexid):
    try:
        materia_texto = MateriaTexto.query.get(mattexid)
        if materia_texto is None:
            return make_response(jsonify({"error": "MateriaTexto not found."}), HTTPStatus.NOT_FOUND)
        db.session.delete(materia_texto)
        db.session.commit()
        return make_response(jsonify({"message": "MateriaTexto deleted successfully."}), HTTPStatus.OK)
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


def getListTextoCombo():
    print("service")
    try:
        # Ejecutar la consulta
        query = db.session.execute('''
            select distinct t.texid, t.texnombre 
            from academico.texto t
            where t.texestado = 1
            order by t.texnombre       
        ''')

        # Obtener los resultados en una lista de diccionarios
        resultados = [{"texid": row.texid, "texnombre": row.texnombre} for row in query]

        # Devolver la respuesta en formato JSON
        return make_response(jsonify(resultados), HTTPStatus.OK)
    except SQLAlchemyError as e:
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)


# Cargar variables de entorno desde el archivo .env
load_dotenv()

def saveFileTexto(request):
    # Configuración inicial
    archivo_key = 'texdocumento'  # Cambia esto según el nombre del campo en tu request
    basepath = os.path.dirname(__file__)

    # Leer las rutas desde las variables de entorno
    static_dir = os.getenv('STATIC_DIR', 'static')
    files_textos_dir = os.getenv('FILES_TEXTOS_DIR', 'files_textos')

    upload_directory = os.path.join(
        basepath, '..', static_dir, files_textos_dir)
    os.makedirs(upload_directory, exist_ok=True)

    archivo = request.files.get(archivo_key)
    if archivo:
        if archivo.filename == '':
            raise ValueError(f"Nombre de archivo vacío para {archivo_key}.")
        if allowedFile(archivo.filename):
            unique_id = str(uuid.uuid4())  # Generar un UUID
            extension = archivo.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{unique_id}.{extension}"
            upload_path = os.path.join(upload_directory, unique_filename)

            # Guardar el archivo solo si no existe
            if not os.path.exists(upload_path):
                archivo.save(upload_path)
            return unique_filename
        else:
            raise ValueError(
                f"Tipo de archivo no permitido para {archivo_key}.")
    return None


def allowedFile(filename):
    # Extensiones permitidas, incluyendo archivos de Word
    allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions



def getListMateriaTextoEstudiante(estudiante_id):
    try:
        # Crear alias para las tablas con aliased
        m = aliased(Materia)
        t = aliased(Texto)
        mt = aliased(MateriaTexto)
        i = aliased(Inscripcion)
        cm = aliased(CursoMateria)
        
        # Realizar la consulta con los joins necesarios, filtrando por el estudiante
        query = (db.session.query(
            mt.mattexid, mt.matid, mt.texid, mt.mattexdescripcion,
            mt.mattexusureg, mt.mattexfecreg, mt.mattexusumod,
            mt.mattexfecmod, mt.mattexestado, m.matnombre, m.matnivel, m.matdesnivel,
            t.texnombre, t.texdocumento, t.texruta, t.texdescripcion
        )
            .join(m, m.matid == mt.matid)
            .join(t, t.texid == mt.texid)
            .join(cm, cm.matid == m.matid)  
            .join(i, i.curmatid == cm.curmatid)  
            .filter(i.peridestudiante == estudiante_id) 
            .order_by(m.matnombre, t.texnombre)
            .distinct()
            .all()
        )

        # Organizar materias y textos en un diccionario agrupado
        materias = {}
        for row in query:
            mat_id = row.matid
            if mat_id not in materias:
                materias[mat_id] = {
                    'materia': row.matnombre,
                    # 'nivel': row.matnivel,
                    # 'desnivel': row.matdesnivel,
                    'textos': []
                }
            
            # Agregar los textos asociados a la materia
            texto = {
                'texid': row.texid,
                'texnombre': row.texnombre,
                'texdocumento': row.texdocumento,
                'texdescripcion': row.texdescripcion,
                'texruta': row.texruta,
                'mattexdescripcion': row.mattexdescripcion,
                'mattexusureg': row.mattexusureg,
                'mattexfecreg': row.mattexfecreg.isoformat() if row.mattexfecreg else None,
                'mattexusumod': row.mattexusumod,
                'mattexfecmod': row.mattexfecmod.isoformat() if row.mattexfecmod else None,
                'mattexestado': row.mattexestado
            }
            materias[mat_id]['textos'].append(texto)
            

        # Convertir el diccionario a una lista para la respuesta
        print("materias", materias)
        
        response = list(materias.values())
        
        return make_response(jsonify(response), HTTPStatus.OK)
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_response = {
            "error": "Error in the database.",
            "message": str(e),
            "code": HTTPStatus.INTERNAL_SERVER_ERROR
        }
        return make_response(jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR)