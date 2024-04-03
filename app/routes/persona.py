from flask_restful import Api
import resources.Persona as Person
import resources.Usuario as Usuario
from client.routes import Routes as routes

def persona_routes(api: Api):
    api.add_resource(Usuario.ListarPersona, routes.listarPersona)
    api.add_resource(Person.GestionarPersona, routes.gestionarPersona)
    api.add_resource(Person.EliminarPersona, routes.eliminarPersona)
    api.add_resource(Person.TipoDocumento, routes.tipoDocumento)
    api.add_resource(Person.TipoEstadoCivil, routes.tipoEstadoCivil)
    api.add_resource(Person.TipoGenero, routes.tipoGenero)
    api.add_resource(Person.TipoPais, routes.tipoPais)
    api.add_resource(Person.TipoCiudad, routes.tipoCiudad)
    api.add_resource(Person.RegistrarPersona, routes.registrarPersona)