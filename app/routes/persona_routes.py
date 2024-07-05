from flask_restful import Api
import resources.Persona_resource as Persona
import resources.Estudiante as Estudiante   
from client.routes import Routes as routes

def persona_routes(api: Api):
    api.add_resource(Persona.ListarPersona, routes.listarPersona)
    api.add_resource(Persona.GestionarPersona, routes.gestionarPersona)
    api.add_resource(Persona.EliminarPersona, routes.eliminarPersona)
    api.add_resource(Persona.TipoDocumento, routes.tipoDocumento)
    api.add_resource(Persona.TipoEstadoCivil, routes.tipoEstadoCivil)
    api.add_resource(Persona.TipoGenero, routes.tipoGenero)
    api.add_resource(Persona.TipoPais, routes.tipoPais)
    api.add_resource(Persona.TipoCiudad, routes.tipoCiudad)
    api.add_resource(Persona.RegistrarPersona, routes.registrarPersona)
    api.add_resource(Estudiante.ActualizarDatosPersonales, routes.actualizarDatosPersonales)
    
    api.add_resource(Persona.ModificarPerfil, routes.modificarPerfil)
    api.add_resource(Persona.MostrarDatosPersona, routes.mostrarDatosPersona)
    
    # Persona Información Personal
    api.add_resource(Persona.ListarInformacionPersonal, routes.informacionPersonal)
    api.add_resource(Persona.AdicionarInformacionPersonal, routes.personaInformacionPersonal)
    api.add_resource(Persona.ModificarInformacionPersonal, routes.informacionPersonal)
    
    # Persona Información Académica
    api.add_resource(Persona.ListarInformacionAcademica, routes.informacionAcademica)
    api.add_resource(Persona.AdicionarInformacionAcademica, routes.personaInformacionAcademica)
    api.add_resource(Persona.ModificarInformacionAcademica, routes.informacionAcademicav2)
    api.add_resource(Persona.EliminarInformacionAcademica, routes.informacionAcademicav2)
    
    # Persona Información Ministerial
    api.add_resource(Persona.ListarInformacionMinisterial, routes.informacionMinisterial)
    api.add_resource(Persona.AdicionarInformacionMinisterial, routes.personaInformacionMinisterial)
    api.add_resource(Persona.ModificarInformacionMinisterial, routes.personaInformacionMinisterialv2)
    
    # Persona Documento Admisión
    api.add_resource(Persona.ListarDocumentoAdmision, routes.documentoAdmision)
    api.add_resource(Persona.AdicionarDocumentoAdmision, routes.personaDocumentoAdmision)
    api.add_resource(Persona.MostrarDocumentoAdmision, routes.documentoAdmisionv2)
    api.add_resource(Persona.ModificarDocumentoAdmision, routes.personaDocumentoAdmision)
    
    # Tipo Profesion
    api.add_resource(Persona.ListarTipoProfesion, routes.tipoProfesion)
    api.add_resource(Persona.AdicionarTipoProfesion, routes.tipoProfesion)
    api.add_resource(Persona.ModificarTipoProfesion, routes.tipoProfesionv2)
    api.add_resource(Persona.EliminarTipoProfesion, routes.tipoProfesionv2)
    
    
    # Tipo Educación
    api.add_resource(Persona.ListarTipoEducacion, routes.tipoEducacion)
    api.add_resource(Persona.AdicionarTipoEducacion, routes.tipoEducacion)
    api.add_resource(Persona.ModificarTipoEducacion, routes.tipoEducacionv2)
    api.add_resource(Persona.EliminarTipoEducacion, routes.tipoEducacionv2)
    
    # Tipo Cargo
    api.add_resource(Persona.ListarTipoCargo, routes.tipoCargo)
    api.add_resource(Persona.AdicionarTipoCargo, routes.tipoCargo)
    api.add_resource(Persona.ModificarTipoCargo, routes.tipoCargov2)
    api.add_resource(Persona.EliminarTipoCargo, routes.tipoCargov2)