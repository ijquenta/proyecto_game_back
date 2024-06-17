from flask_restful import Api
import resources.Persona_resource as Persona
import resources.Usuario as Usuario
from client.routes import Routes as routes

def usuario_routes(api: Api):
    api.add_resource(Persona.ListarUsuarios, routes.listaUsuarios)
    api.add_resource(Usuario.GestionarUsuario, routes.gestionarUsuario)
    api.add_resource(Usuario.ListaUsuario, routes.listaUsuario)
    api.add_resource(Usuario.TipoPersona, routes.tipoPersona)
    api.add_resource(Usuario.Perfil, routes.perfil)
    api.add_resource(Usuario.ObtenerEmail, routes.obtenerEmail)
    api.add_resource(Usuario.GestionarUsuarioEstado, routes.gestionarUsuarioEstado)
    api.add_resource(Usuario.GestionarUsuarioPassword, routes.gestionarUsuarioPassword)