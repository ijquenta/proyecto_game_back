from flask_restful import Resource, reqparse
from flask import request
from services.texto_service import *  # Importa tus funciones de servicio
from resources.Autenticacion import token_required

parseCreateTipoExtensionTexto = reqparse.RequestParser()
parseCreateTipoExtensionTexto.add_argument('tipextnombre', type=str, help='Ingrese nombre del tipo de extensión de texto', required=True)

parseUpdateTipoExtensionTexto = reqparse.RequestParser()
parseUpdateTipoExtensionTexto.add_argument('tipextnombre', type=str, help='Ingrese nombre del tipo de extensión de texto', required=True)
parseUpdateTipoExtensionTexto.add_argument('tipextusuario', type=str, help='Ingrese usuario de modificación', required=True)
class GetListTipoExtensionTexto(Resource):
    @token_required
    def get(self):
        return getListTipoExtensionTexto()

class CreateTipoExtensionTexto(Resource):
    @token_required
    def post(self):
        data = parseCreateTipoExtensionTexto.parse_args()
        return createTipoExtensionTexto(data)

class UpdateTipoExtensionTexto(Resource):
    @token_required
    def put(self, tipextid):
        data = parseUpdateTipoExtensionTexto.parse_args()
        return updateTipoExtensionTexto(data, tipextid) 

class DeleteTipoExtensionTexto(Resource):
    @token_required
    def delete(self, tipextid):
        return deleteTipoExtensionTexto(tipextid)


# Parseadores de argumentos para TipoTexto
parseCreateTipoTexto = reqparse.RequestParser()
parseCreateTipoTexto.add_argument('tiptexnombre', type=str, help='Ingrese nombre del tipo de texto', required=True)

parseUpdateTipoTexto = reqparse.RequestParser()
parseUpdateTipoTexto.add_argument('tiptexnombre', type=str, help='Ingrese nombre del tipo de texto', required=True)

class GetListTipoTexto(Resource):
    @token_required
    def get(self):
        return getListTipoTexto()

class CreateTipoTexto(Resource):
    @token_required
    def post(self):
        data = parseCreateTipoTexto.parse_args()
        return createTipoTexto(data)

class UpdateTipoTexto(Resource):
    @token_required
    def put(self, tiptexid):
        data = parseUpdateTipoTexto.parse_args()
        return updateTipoTexto(data, tiptexid)

class DeleteTipoTexto(Resource):
    @token_required
    def delete(self, tiptexid):
        return deleteTipoTexto(tiptexid)



# Parseadores de argumentos para TipoIdiomaTexto
parseCreateTipoIdiomaTexto = reqparse.RequestParser()
parseCreateTipoIdiomaTexto.add_argument('tipidinombre', type=str, help='Ingrese nombre del tipo de idioma texto', required=True)

parseUpdateTipoIdiomaTexto = reqparse.RequestParser()
parseUpdateTipoIdiomaTexto.add_argument('tipidinombre', type=str, help='Ingrese nombre del tipo de idioma texto', required=True)

class GetListTipoIdiomaTexto(Resource):
    @token_required
    def get(self):
        return getListTipoIdiomaTexto()

class CreateTipoIdiomaTexto(Resource):
    @token_required
    def post(self):
        data = parseCreateTipoIdiomaTexto.parse_args()
        return createTipoIdiomaTexto(data)

class UpdateTipoIdiomaTexto(Resource):
    @token_required
    def put(self, tipidiid):
        data = parseUpdateTipoIdiomaTexto.parse_args()
        return updateTipoIdiomaTexto(data, tipidiid)

class DeleteTipoIdiomaTexto(Resource):
    @token_required
    def delete(self, tipidiid):
        return deleteTipoIdiomaTexto(tipidiid)
    
    
# Parseadores de argumentos para TipoCategoriaTexto
parseCreateTipoCategoriaTexto = reqparse.RequestParser()
parseCreateTipoCategoriaTexto.add_argument('tipcatnombre', type=str, help='Ingrese nombre del tipo de categoría texto', required=True)

parseUpdateTipoCategoriaTexto = reqparse.RequestParser()
parseUpdateTipoCategoriaTexto.add_argument('tipcatnombre', type=str, help='Ingrese nombre del tipo de categoría texto', required=True)

class GetListTipoCategoriaTexto(Resource):
    @token_required
    def get(self):
        return getListTipoCategoriaTexto()

class CreateTipoCategoriaTexto(Resource):
    @token_required
    def post(self):
        data = parseCreateTipoCategoriaTexto.parse_args()
        return createTipoCategoriaTexto(data)

class UpdateTipoCategoriaTexto(Resource):
    @token_required
    def put(self, tipcatid):
        data = parseUpdateTipoCategoriaTexto.parse_args()
        return updateTipoCategoriaTexto(data, tipcatid)

class DeleteTipoCategoriaTexto(Resource):
    @token_required
    def delete(self, tipcatid):
        return deleteTipoCategoriaTexto(tipcatid)
    
    
    
# Parseadores de argumentos para Texto
parseCreateTexto = reqparse.RequestParser()
parseCreateTexto.add_argument('texnombre', type=str, help='Ingrese nombre del texto', required=True)
parseCreateTexto.add_argument('textipo', type=str, help='Ingrese tipo del texto')
parseCreateTexto.add_argument('texformato', type=int, help='Ingrese formato del texto')
parseCreateTexto.add_argument('texdocumento', type=str, help='Ingrese documento del texto')
parseCreateTexto.add_argument('texruta', type=str, help='Ingrese ruta del texto')
parseCreateTexto.add_argument('texdescripcion', type=str, help='Ingrese descripción del texto')
parseCreateTexto.add_argument('texautor', type=str, help='Ingrese autor del texto')
parseCreateTexto.add_argument('texsize', type=int, help='Ingrese tamaño del texto')
parseCreateTexto.add_argument('texextension', type=int, help='Ingrese extensión del texto')
parseCreateTexto.add_argument('texidioma', type=int, help='Ingrese idioma del texto')
parseCreateTexto.add_argument('texfecpublicacion', type=str, help='Ingrese fecha de publicación del texto')
parseCreateTexto.add_argument('texcategoria', type=int, help='Ingrese categoría del texto')
parseCreateTexto.add_argument('texusureg', type=str, help='Ingrese usuario de registro', required=True)
parseCreateTexto.add_argument('texestado', type=int, help='Ingrese estado del texto', required=True)

parseUpdateTexto = reqparse.RequestParser()
parseUpdateTexto.add_argument('texnombre', type=str, help='Ingrese nombre del texto')
parseUpdateTexto.add_argument('textipo', type=str, help='Ingrese tipo del texto')
parseUpdateTexto.add_argument('texformato', type=int, help='Ingrese formato del texto')
parseUpdateTexto.add_argument('texdocumento', type=str, help='Ingrese documento del texto')
parseUpdateTexto.add_argument('texruta', type=str, help='Ingrese ruta del texto')
parseUpdateTexto.add_argument('texdescripcion', type=str, help='Ingrese descripción del texto')
parseUpdateTexto.add_argument('texautor', type=str, help='Ingrese autor del texto')
parseUpdateTexto.add_argument('texsize', type=int, help='Ingrese tamaño del texto')
parseUpdateTexto.add_argument('texextension', type=int, help='Ingrese extensión del texto')
parseUpdateTexto.add_argument('texidioma', type=int, help='Ingrese idioma del texto')
parseUpdateTexto.add_argument('texfecpublicacion', type=str, help='Ingrese fecha de publicación del texto')
parseUpdateTexto.add_argument('texcategoria', type=int, help='Ingrese categoría del texto')
parseUpdateTexto.add_argument('texusumod', type=str, help='Ingrese usuario de modificación', required=True)
parseUpdateTexto.add_argument('texestado', type=int, help='Ingrese estado del texto', required=True)

class GetListTexto(Resource):
    @token_required
    def get(self):
        return getListTexto()

class CreateTexto(Resource):
    @token_required
    def post(self):
        data = parseCreateTexto.parse_args()
        return createTexto(data, request)

class UpdateTexto(Resource):
    @token_required
    def put(self, texid):
        data = parseUpdateTexto.parse_args()
        return updateTexto(data, texid, request)

class DeleteTexto(Resource):
    @token_required
    def delete(self, texid):
        return deleteTexto(texid)


# Parseadores de argumentos para MateriaTexto
parseCreateMateriaTexto = reqparse.RequestParser()
parseCreateMateriaTexto.add_argument('matid', type=int, help='Ingrese ID de materia', required=True)
parseCreateMateriaTexto.add_argument('texid', type=int, help='Ingrese ID de texto', required=True)
parseCreateMateriaTexto.add_argument('mattexdescripcion', type=str, help='Ingrese descripción del texto-materia')
parseCreateMateriaTexto.add_argument('mattexusureg', type=str, help='Ingrese usuario de registro', required=True)
parseCreateMateriaTexto.add_argument('mattexestado', type=int, help='Ingrese estado del texto-materia', required=True)

parseUpdateMateriaTexto = reqparse.RequestParser()
parseUpdateMateriaTexto.add_argument('matid', type=int, help='Ingrese ID de materia', required=True)
parseUpdateMateriaTexto.add_argument('texid', type=int, help='Ingrese ID de texto', required=True)
parseUpdateMateriaTexto.add_argument('mattexdescripcion', type=str, help='Ingrese descripción del texto-materia')
parseUpdateMateriaTexto.add_argument('mattexusumod', type=str, help='Ingrese usuario de modificación', required=True)
parseUpdateMateriaTexto.add_argument('mattexestado', type=int, help='Ingrese estado del texto-materia', required=True)

class GetListMateriaTexto(Resource):
    @token_required
    def get(self):
        return getListMateriaTexto()
    
class GetListMateriaTextoEstudiante(Resource):
    @token_required
    def get(self, peridestudiante):
        return getListMateriaTextoEstudiante(peridestudiante)

class CreateMateriaTexto(Resource):
    @token_required
    def post(self):
        data = parseCreateMateriaTexto.parse_args()
        return createMateriaTexto(data)

class UpdateMateriaTexto(Resource):
    @token_required
    def put(self, mattexid):
        data = parseUpdateMateriaTexto.parse_args()
        return updateMateriaTexto(data, mattexid)

class DeleteMateriaTexto(Resource):
    @token_required
    def delete(self, mattexid):
        return deleteMateriaTexto(mattexid)