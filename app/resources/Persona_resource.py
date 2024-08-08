from flask_restful import Resource, reqparse  
from flask import request  
from services.persona_service import *  
from resources.Autenticacion import token_required  

# Section Person

parseCreatePersonForm = reqparse.RequestParser()
parseCreatePersonForm.add_argument('pernombres', type=str, help='Nombres de la persona', required=True)
parseCreatePersonForm.add_argument('perapepat', type=str, help='Apellido paterno de la persona', required=True)
parseCreatePersonForm.add_argument('perapemat', type=str, help='Apellido materno de la persona', required=True)
parseCreatePersonForm.add_argument('pertipodoc', type=int, help='Tipo de documento de la persona', required=True)
parseCreatePersonForm.add_argument('pernrodoc', type=str, help='Número de documento de la persona', required=True)
parseCreatePersonForm.add_argument('peremail', type=str, help='este campo es requerido peremail', required=True)
parseCreatePersonForm.add_argument('perusureg', type=str, help='este campo es requerido perusureg', required=True)
parseCreatePersonForm.add_argument('perobservacion', type=str, help='este campo es requerido perobservacion', required=True)
class CreatePersonForm(Resource):
    def post(self):
        data = parseCreatePersonForm.parse_args()
        return createPersonForm(data)

# Manage Person

parseManagePerson = reqparse.RequestParser()
parseManagePerson.add_argument('tipo', type=int, help='Tipo de operación', required=True)
parseManagePerson.add_argument('perid', type=int, help='ID de la persona')
parseManagePerson.add_argument('pernombres', type=str, help='Nombres de la persona', required=True)
parseManagePerson.add_argument('perapepat', type=str, help='Apellido paterno de la persona', required=True)
parseManagePerson.add_argument('perapemat', type=str, help='Apellido materno de la persona', required=True)
parseManagePerson.add_argument('pertipodoc', type=int, help='Tipo de documento de la persona', required=True)
parseManagePerson.add_argument('pernrodoc', type=str, help='Número de documento de la persona')
parseManagePerson.add_argument('perfecnac', type=str, help='Fecha de nacimiento de la persona')
parseManagePerson.add_argument('perdirec', type=str, help='Dirección de la persona', required=True)
parseManagePerson.add_argument('peremail', type=str, help='Correo electrónico de la persona', required=True)
parseManagePerson.add_argument('percelular', type=str, help='Número de celular de la persona', required=True)
parseManagePerson.add_argument('pertelefono', type=str, help='Número de teléfono de la persona', required=True)
parseManagePerson.add_argument('perpais', type=int, help='ID del país de la persona', required=True)
parseManagePerson.add_argument('perciudad', type=int, help='ID de la ciudad de la persona', required=True)
parseManagePerson.add_argument('pergenero', type=int, help='ID del género de la persona', required=True)
parseManagePerson.add_argument('perestcivil', type=int, help='ID del estado civil de la persona', required=True)
parseManagePerson.add_argument('perestado', type=int, help='Estado de la persona')
parseManagePerson.add_argument('perobservacion', type=str, help='Observaciones sobre la persona')
parseManagePerson.add_argument('perusureg', type=str, help='Usuario que registró la persona')
parseManagePerson.add_argument('perusumod', type=str, help='Usuario que modificó la persona')

# Delete Person
parseDeletePerson = reqparse.RequestParser()
parseDeletePerson.add_argument('tipo', type=int, help='Tipo de operación', required=True)
parseDeletePerson.add_argument('perid', type=int, help='ID de la persona', required=True)
parseDeletePerson.add_argument('perusumod', type=str, help='Usuario que modificó la persona', required=True)

class GetPersons(Resource):
    # @     CreatePersonForm
    def get(self):
        return getPersons()

class ManagePerson(Resource):
    @token_required
    def post(self):
        data = parseManagePerson.parse_args()
        return managePerson(data, request)
    
class DeletePerson(Resource):
    @token_required
    def post(self):
        data = parseDeletePerson.parse_args()
        return deletePerson(data)               
    
class DeletePersonForm(Resource):
    def delete(self, perid):
        return deletePersonForm(perid)
    
# Sección Persona Información Personal

parseAdicionarInformacionPersonal = reqparse.RequestParser()
parseAdicionarInformacionPersonal.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseAdicionarInformacionPersonal.add_argument('peredad', type=int, help='Ingrese peredad', required=True)
parseAdicionarInformacionPersonal.add_argument('pernrohijos', type=int, help='Ingrese pernrohijos', required=True)
parseAdicionarInformacionPersonal.add_argument('perprofesion', type=int, help='Ingrese perprofesion', required=True)
parseAdicionarInformacionPersonal.add_argument('perlugconversion', type=str, help='Ingrese perlugconversion', required=True)
parseAdicionarInformacionPersonal.add_argument('perfecconversion', type=str, help='Ingrese perfecconversion', required=True)
parseAdicionarInformacionPersonal.add_argument('perbautizoagua', type=int, help='Ingrese perbautizoagua', required=True)
parseAdicionarInformacionPersonal.add_argument('perbautizoespiritu', type=int, help='Ingrese perbautizoespiritu', required=True)
parseAdicionarInformacionPersonal.add_argument('pernomiglesia', type=str, help='Ingrese pernomiglesia', required=True)
parseAdicionarInformacionPersonal.add_argument('perdiriglesia',  type=str, help='Ingrese perdiriglesia', required=True)
parseAdicionarInformacionPersonal.add_argument('pernompastor', type=str, help='Ingrese pernompastor', required=True)
parseAdicionarInformacionPersonal.add_argument('percelpastor', type=str, help='Ingrese percelpastor', required=True)
parseAdicionarInformacionPersonal.add_argument('perusureg', type=str, help='Ingrese perusureg', required=True)
parseAdicionarInformacionPersonal.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True) 
parseAdicionarInformacionPersonal.add_argument('perestado', type=int, help='Ingrese perestado', required=True)
parseAdicionarInformacionPersonal.add_argument('perexperiencia', type=int, help='Ingrese perexperiencia', required=True)
parseAdicionarInformacionPersonal.add_argument('permotivo', type=str, help='Ingrese permotivo', required=True)
parseAdicionarInformacionPersonal.add_argument('perplanesmetas', type=str, help='Ingrese perplanesmetas', required=True)

parseModificarInformacionPersonal = reqparse.RequestParser()
parseModificarInformacionPersonal.add_argument('peredad', type=int, help='Ingrese peredad', required=True)
parseModificarInformacionPersonal.add_argument('pernrohijos', type=int, help='Ingrese pernrohijos', required=True)
parseModificarInformacionPersonal.add_argument('perprofesion', type=int, help='Ingrese perprofesion', required=True)
parseModificarInformacionPersonal.add_argument('perlugconversion', type=str, help='Ingrese perlugconversion', required=True)
parseModificarInformacionPersonal.add_argument('perfecconversion', type=str, help='Ingrese perfecconversion', required=True)
parseModificarInformacionPersonal.add_argument('perbautizoagua', type=int, help='Ingrese perbautizoagua', required=True)
parseModificarInformacionPersonal.add_argument('perbautizoespiritu', type=int, help='Ingrese perbautizoespiritu', required=True)
parseModificarInformacionPersonal.add_argument('pernomiglesia', type=str, help='Ingrese pernomiglesia', required=True)
parseModificarInformacionPersonal.add_argument('perdiriglesia',  type=str, help='Ingrese perdiriglesia', required=True)
parseModificarInformacionPersonal.add_argument('pernompastor', type=str, help='Ingrese pernompastor', required=True)
parseModificarInformacionPersonal.add_argument('percelpastor', type=str, help='Ingrese percelpastor', required=True)
parseModificarInformacionPersonal.add_argument('perusumod', type=str, help='Ingrese perusumod', required=True)
parseModificarInformacionPersonal.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True) 
parseModificarInformacionPersonal.add_argument('perestado', type=int, help='Ingrese perestado', required=True)
parseModificarInformacionPersonal.add_argument('perexperiencia', type=int, help='Ingrese perexperiencia', required=True)
parseModificarInformacionPersonal.add_argument('permotivo', type=str, help='Ingrese permotivo', required=True)
parseModificarInformacionPersonal.add_argument('perplanesmetas', type=str, help='Ingrese perplanesmetas', required=True)

class ListarInformacionPersonal(Resource):
    @token_required
    def get(self, perid):
        return listarInformacionPersonal(perid)

class AdicionarInformacionPersonal(Resource):
    @token_required
    def post(self):
        data = parseAdicionarInformacionPersonal.parse_args()
        return adicionarInformacionPersonal(data)

class ModificarInformacionPersonal(Resource):
    @token_required
    def put(self, perid):
        data = parseModificarInformacionPersonal.parse_args()
        return modificarInformacionPersonal(data, perid)    


# Sección Persona Información Académica

parseAdicionarInformacionAcademica = reqparse.RequestParser()
parseAdicionarInformacionAcademica.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseAdicionarInformacionAcademica.add_argument('pereducacion', type=int, help='Ingrese pereducacion', required=True)
parseAdicionarInformacionAcademica.add_argument('pernominstitucion', type=str, help='Ingrese pernominstitucion', required=True)
parseAdicionarInformacionAcademica.add_argument('perdirinstitucion', type=str, help='Ingrese perdirinstitucion', required=True)
parseAdicionarInformacionAcademica.add_argument('pergescursadas', type=str, help='Ingrese pergescursadas', required=True)
parseAdicionarInformacionAcademica.add_argument('perfechas', type=str, help='Ingrese perfechas', required=True)
parseAdicionarInformacionAcademica.add_argument('pertitulo', type=str, help='Ingrese pertitulo', required=True)
parseAdicionarInformacionAcademica.add_argument('perusureg', type=str, help='Ingrese perusureg', required=True)
parseAdicionarInformacionAcademica.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True) 
parseAdicionarInformacionAcademica.add_argument('perestado', type=int, help='Ingrese perestado', required=True)

parseModificarInformacionAcademica = reqparse.RequestParser()
parseModificarInformacionAcademica.add_argument('pereducacion', type=int, help='Ingrese pereducacion', required=True)
parseModificarInformacionAcademica.add_argument('pernominstitucion', type=str, help='Ingrese pernominstitucion', required=True)
parseModificarInformacionAcademica.add_argument('perdirinstitucion', type=str, help='Ingrese perdirinstitucion', required=True)
parseModificarInformacionAcademica.add_argument('pergescursadas', type=str, help='Ingrese pergescursadas', required=True)
parseModificarInformacionAcademica.add_argument('perfechas', type=str, help='Ingrese perfechas', required=True)
parseModificarInformacionAcademica.add_argument('pertitulo', type=str, help='Ingrese pertitulo', required=True)
parseModificarInformacionAcademica.add_argument('perusumod', type=str, help='Ingrese perusumod          ', required=True)
parseModificarInformacionAcademica.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True) 
parseModificarInformacionAcademica.add_argument('perestado', type=int, help='Ingrese perestado', required=True)

class ListarInformacionAcademica(Resource):
    @token_required
    def get(self, perid):
        return listarInformacionAcademica(perid)
    
class AdicionarInformacionAcademica(Resource):
    @token_required
    def post(self):
        data = parseAdicionarInformacionAcademica.parse_args()
        return adicionarInformacionAcademica(data)
    
class ModificarInformacionAcademica(Resource):
    @token_required
    def put(self, perinfoaca):
        data = parseModificarInformacionAcademica.parse_args()
        return modificarInformacionAcademica(data, perinfoaca)
    
class EliminarInformacionAcademica(Resource):
    @token_required
    def delete(self, perinfoaca):
        return eliminarInformacionAcademica(perinfoaca)


# Sección Persona Información Ministerial

parseAdicionarInformacionMinisterial = reqparse.RequestParser()
parseAdicionarInformacionMinisterial.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseAdicionarInformacionMinisterial.add_argument('pernomiglesia', type=str, help='Ingrese pernomiglesia', required=True)
parseAdicionarInformacionMinisterial.add_argument('percargo', type=int, help='Ingrese percargo', required=True)
parseAdicionarInformacionMinisterial.add_argument('pergestion', type=int, help='Ingrese pergestion', required=True)
parseAdicionarInformacionMinisterial.add_argument('perusureg', type=str, help='Ingrese perusureg', required=True)
parseAdicionarInformacionMinisterial.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True) 
parseAdicionarInformacionMinisterial.add_argument('perestado', type=int, help='Ingrese perestado', required=True)

parseModificarInformacionMinisterial = reqparse.RequestParser()
parseModificarInformacionMinisterial.add_argument('pernomiglesia', type=str, help='Ingrese pernomiglesia', required=True)
parseModificarInformacionMinisterial.add_argument('percargo', type=int, help='Ingrese percargo', required=True)
parseModificarInformacionMinisterial.add_argument('pergestion', type=int, help='Ingrese pergestion', required=True)
parseModificarInformacionMinisterial.add_argument('perusumod', type=str, help='Ingrese perusumod', required=True)
parseModificarInformacionMinisterial.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True) 
parseModificarInformacionMinisterial.add_argument('perestado', type=int, help='Ingrese perestado', required=True)

class ListarInformacionMinisterial(Resource):
  @token_required
  def get(self, perid):
      return listarInformacionMinisterial(perid)

class AdicionarInformacionMinisterial(Resource):
    @token_required
    def post(self):
        data = parseAdicionarInformacionMinisterial.parse_args()
        return adicionarInformacionMinisterial(data)
    
class ModificarInformacionMinisterial(Resource):
    @token_required
    def put(self, perinfomin):
        data = parseModificarInformacionMinisterial.parse_args()
        return modificarInformacionMinisterial(data, perinfomin)

# Sección Documento admisión

parseAdicionarDocumentoAdmision = reqparse.RequestParser()
parseAdicionarDocumentoAdmision.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseAdicionarDocumentoAdmision.add_argument('perusureg', type=str, help='Ingrese perusureg', required=True)
parseAdicionarDocumentoAdmision.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True)
parseAdicionarDocumentoAdmision.add_argument('perestado', type=int, help='Ingrese perestado', required=True)

parseModificarDocumentoAdmision = reqparse.RequestParser()
parseModificarDocumentoAdmision.add_argument('perid', type=int, help='Ingrese perid', required=True)
parseModificarDocumentoAdmision.add_argument('perusumod', type=str, help='Ingrese perusumod', required=True)
parseModificarDocumentoAdmision.add_argument('perobservacion', type=str, help='Ingrese perobservacion', required=True)
parseModificarDocumentoAdmision.add_argument('perestado', type=int, help='Ingrese perestado', required=True)

class ListarDocumentoAdmision(Resource):
    @token_required
    def get(self, perid):
        return listarDocumentoAdmision(perid)    

class AdicionarDocumentoAdmision(Resource):
    @token_required
    def post(self):
        data = parseAdicionarDocumentoAdmision.parse_args() 
        return adicionarDocumentoAdmision(data, request)

class ModificarDocumentoAdmision(Resource):
    @token_required
    def put(self):
        data = parseModificarDocumentoAdmision.parse_args() 
        return modificarDocumentoAdmision(data, request)    
                                            
class MostrarDocumentoAdmision(Resource):
    # @token_required
    def get(self, filename):
        return mostrarDocumentoAdmision(filename)
        

    
# Seccción Tipo Profesion 

parseAdicionarTipoProfesion = reqparse.RequestParser()
parseAdicionarTipoProfesion.add_argument('pronombre', type=str, help='Ingrese pronombre', required=True)
parseAdicionarTipoProfesion.add_argument('prousureg', type=str, help='Ingrese prousureg', required=True)
parseAdicionarTipoProfesion.add_argument('proobservacion', type=str, help='Ingrese proobservacion', required=True)
parseAdicionarTipoProfesion.add_argument('proestado', type=int, help='Ingrese proestado', required=True)

parseModificarTipoProfesion = reqparse.RequestParser()
parseModificarTipoProfesion.add_argument('pronombre', type=str, help='Ingrese pronombre', required=True)
parseModificarTipoProfesion.add_argument('prousumod', type=str, help='Ingrese prousumod', required=True)  
parseModificarTipoProfesion.add_argument('proobservacion', type=str, help='Ingrese proobservacion', required=True)      
parseModificarTipoProfesion.add_argument('proestado', type=int, help='Ingrese proestado', required=True)

class ListarTipoProfesion(Resource):
    @token_required
    def get(self):
        return listarTipoProfesion()

class AdicionarTipoProfesion(Resource):     
    @token_required
    def post(self):
        data = parseAdicionarTipoProfesion.parse_args()
        return adicionarTipoProfesion(data)      

class ModificarTipoProfesion(Resource):
    @token_required
    def put(self, proid):
        data = parseModificarTipoProfesion.parse_args()
        return modificarTipoProfesion(data, proid) 

class EliminarTipoProfesion(Resource):
    @token_required
    def delete(self, proid):
        return eliminarTipoProfesion(proid)


# Sección Tipo Educación

parseAdicionarTipoEducacion = reqparse.RequestParser()
parseAdicionarTipoEducacion.add_argument('edunombre', type=str, help='Ingrese edunombre', required=True)
parseAdicionarTipoEducacion.add_argument('eduusureg', type=str, help='Ingrese eduusureg', required=True)
parseAdicionarTipoEducacion.add_argument('eduobservacion', type=str, help='Ingrese eduobservacion', required=True)
parseAdicionarTipoEducacion.add_argument('eduestado', type=int, help='Ingrese eduestado', required=True)

parseModificarTipoEducacion = reqparse.RequestParser()
parseModificarTipoEducacion.add_argument('edunombre', type=str, help='Ingrese edunombre', required=True)
parseModificarTipoEducacion.add_argument('eduusumod', type=str, help='Ingrese eduusumod', required=True)  
parseModificarTipoEducacion.add_argument('eduobservacion', type=str, help='Ingrese eduobservacion', required=True)      
parseModificarTipoEducacion.add_argument('eduestado', type=int, help='Ingrese eduestado', required=True)

class ListarTipoEducacion(Resource):
    @token_required
    def get(self):
        return listarTipoEducacion()

class AdicionarTipoEducacion(Resource):
    @token_required
    def post(self):
        data = parseAdicionarTipoEducacion.parse_args()
        return adicionarTipoEducacion(data)

class ModificarTipoEducacion(Resource):
    @token_required
    def put(self, eduid):
        data = parseModificarTipoEducacion.parse_args()
        return modificarTipoEducacion(data, eduid) 

class EliminarTipoEducacion(Resource):
    @token_required
    def delete(self, eduid):
        return eliminarTipoEducacion(eduid)
    
# Sección Tipo Cargo

parseAdicionarTipoCargo = reqparse.RequestParser()
parseAdicionarTipoCargo.add_argument('carnombre', type=str, help='Ingrese carnombre', required=True)
parseAdicionarTipoCargo.add_argument('carusureg', type=str, help='Ingrese carusureg', required=True)
parseAdicionarTipoCargo.add_argument('carobservacion', type=str, help='Ingrese carobservacion', required=True)
parseAdicionarTipoCargo.add_argument('carestado', type=int, help='Ingrese carestado', required=True)

parseModificarTipoCargo = reqparse.RequestParser()
parseModificarTipoCargo.add_argument('carnombre', type=str, help='Ingrese carnombre', required=True)
parseModificarTipoCargo.add_argument('carusumod', type=str, help='Ingrese carusumod', required=True)
parseModificarTipoCargo.add_argument('carobservacion', type=str, help='Ingrese carobservacion', required=True)
parseModificarTipoCargo.add_argument('carestado', type=int, help='Ingrese carestado', required=True)

class ListarTipoCargo(Resource):
    @token_required
    def get(self):
        return listarTipoCargo()

class AdicionarTipoCargo(Resource):
    @token_required
    def post(self):
        data = parseAdicionarTipoCargo.parse_args()
        return adicionarTipoCargo(data)
    
class ModificarTipoCargo(Resource):
    @token_required
    def put(self, carid):
        data = parseModificarTipoCargo.parse_args()
        return modificarTipoCargo(data, carid)
    
class EliminarTipoCargo(Resource):
    @token_required
    def delete(self, carid):
        return eliminarTipoCargo(carid)


# Sección Actualizar Perfil

parseupdateProfile = reqparse.RequestParser()
parseupdateProfile.add_argument('perid', type=int, help='se requiere perid', required=True)
parseupdateProfile.add_argument('pernombres', type=str, help='se requiere pernombres', required=True)
parseupdateProfile.add_argument('perapepat', type=str, help='se requiere perapepat', required=True)
parseupdateProfile.add_argument('perapemat', type=str, help='se requiere perapemat', required=True)
parseupdateProfile.add_argument('pertipodoc', type=int, help='se requiere pertipodoc', required=True)
parseupdateProfile.add_argument('pernrodoc', type=str, help='se requiere pernrodoc', required=True)
parseupdateProfile.add_argument('perfecnac', type=str, help='se requiere perfecnac', required=True)
parseupdateProfile.add_argument('perdirec', type=str, help='se requiere perdirec', required=True)
parseupdateProfile.add_argument('peremail', type=str, help='se requiere peremail', required=True)
parseupdateProfile.add_argument('percelular', type=str, help='se requiere percelular', required=True)
parseupdateProfile.add_argument('pertelefono', type=str, help='se requiere pertelefono', required=True)
parseupdateProfile.add_argument('perpais', type=int, help='se requiere perpais', required=True)
parseupdateProfile.add_argument('perciudad', type=int, help='se requiere perciudad', required=True)
parseupdateProfile.add_argument('pergenero', type=int, help='se requiere pergenero', required=True)
parseupdateProfile.add_argument('perestcivil', type=int, help='se requiere perestcivil', required=True)
parseupdateProfile.add_argument('perusumod', type=str, help='se requiere perusumod', required=True)

class UpdateProfile(Resource):
    @token_required
    def post(self):
        data = parseupdateProfile.parse_args()
        return updateProfile(data, request)
    
class ShowPersonData(Resource):
    @token_required
    def get(self, perid):
        return showPersonData(perid)

# Section Types   

class TipoDocumento(Resource):
    def get(self):
        return tipoDocumento()

class TipoGenero(Resource):
    def get(self):
        return tipoGenero()

class TipoPais(Resource):
    def get(self):
        return tipoPais()

class TipoCiudad(Resource):
    def get(self):
        return tipoCiudad()

class TipoEstadoCivil(Resource):
    def get(self):
        return tipoEstadoCivil()

class ListarUsuarios(Resource):
    @token_required
    def get(self):
        return listarUsuarios() 

class GetUsers(Resource):
    def get(self):
        return getUsers() 


