from flask_restful import Api
from flask_mail import Mail
import resources.Persona_resource as Persona
import resources.Usuario as Usuario


from client.routes import Routes as routes

def usuario_routes(api: Api, mail: Mail):
    api.add_resource(Persona.ListarUsuarios, routes.listaUsuarios)
    api.add_resource(Persona.GetUsers, routes.getUsers)
    api.add_resource(Usuario.GestionarUsuario, routes.gestionarUsuario)
    api.add_resource(Usuario.ListaUsuario, routes.listaUsuario)
    api.add_resource(Usuario.TipoPersona, routes.tipoPersona)
    api.add_resource(Usuario.Perfil, routes.perfil)
    api.add_resource(Usuario.ObtenerEmail, routes.obtenerEmail)
    api.add_resource(Usuario.GestionarUsuarioEstado, routes.gestionarUsuarioEstado)
    api.add_resource(Usuario.GestionarUsuarioPassword, routes.gestionarUsuarioPassword)
    api.add_resource(Usuario.ResetPasswordResource, routes.resetPassword)
    api.add_resource(Usuario.RequestChangePassword, routes.requestChangePassword, resource_class_args=(mail,))
    api.add_resource(Usuario.BuscarUsuario, routes.buscarUsuario)
    api.add_resource(Usuario.ChangePasswordResource, routes.changePassword)