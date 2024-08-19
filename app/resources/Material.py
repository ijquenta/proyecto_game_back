from flask_restful import Resource, reqparse
from services.material_service import * # Servicio de material de apoyo
from resources.Autenticacion import token_required

class GetListTextoCombo(Resource):
    @token_required
    def get(self):
      return getListTextoCombo()
    
"""
class ListarMaterial(Resource):
    # @token_required
    def get(self):
        return listarMaterial()

class ListarTexto(Resource):
    # @token_required
    def get(self):
        return listarTexto()

# Insertar Texto
parseInsertarTexto = reqparse.RequestParser()
parseInsertarTexto.add_argument('texnombre', type=str, help='Ingrese textnombre', required=True)
parseInsertarTexto.add_argument('textipo', type=str, help='Ingrese textipo', required=True)
parseInsertarTexto.add_argument('texdocumento', type=str, help='Ingrese texdocumento', required=True)
parseInsertarTexto.add_argument('texusureg', type=str, help='Ingrese textusureg', required=True)
class InsertarTexto(Resource):
    # @token_required
    def post(self):
        data = parseInsertarTexto.parse_args()
        return insertarTexto(data)
    
    
class ListarMateriaTexto(Resource):
    # @token_required
    def get(self):
        return listarMateriaTexto()
    

    
# Insertar Materia Texto
parseInsertarMateriaTexto = reqparse.RequestParser()
parseInsertarMateriaTexto.add_argument('matid', type=int, help='Ingrese ID de la materia', required=True)
parseInsertarMateriaTexto.add_argument('texid', type=int, help='Ingrese ID del texto', required=True)
parseInsertarMateriaTexto.add_argument('mattexdescripcion', type=str, help='Ingrese descripción', required=True)
parseInsertarMateriaTexto.add_argument('mattexusureg', type=str, help='Ingrese usuario de registro', required=True)

class InsertarMateriaTexto(Resource):
    def post(self):
        data = parseInsertarMateriaTexto.parse_args()
        return insertarMateriaTexto(data)

# Modificar Materia Texto
parseModificarMateriaTexto = reqparse.RequestParser()
parseModificarMateriaTexto.add_argument('mattexid', type=int, help='Ingrese ID del registro', required=True)
parseModificarMateriaTexto.add_argument('matid', type=int, help='Ingrese ID de la materia', required=True)
parseModificarMateriaTexto.add_argument('texid', type=int, help='Ingrese ID del texto', required=True)
parseModificarMateriaTexto.add_argument('mattexdescripcion', type=str, help='Ingrese nueva descripción', required=True)
parseModificarMateriaTexto.add_argument('mattexusumod', type=str, help='Ingrese usuario de modificación', required=True)

class ModificarMateriaTexto(Resource):
    def post(self):
        data = parseModificarMateriaTexto.parse_args()
        return modificarMateriaTexto(data)
"""
