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