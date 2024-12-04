from flask_restful import Api
import resources.Persona_resource as Persona
import resources.Usuario as Usuario

apiVersion = "/v1"


from client.routes import Routes as routes

def usuario_routes(api: Api):
    api.add_resource(Persona.ListarUsuarios, routes.listaUsuarios)
    api.add_resource(Persona.GetUsers, routes.getUsers)
    api.add_resource(Usuario.GestionarUsuario, routes.gestionarUsuario)
    api.add_resource(Usuario.ListaUsuario, routes.listaUsuario)
    api.add_resource(Usuario.TipoPersona, routes.tipoPersona)
    api.add_resource(Usuario.TipoPersonaDocente, routes.tipoPersonaDocente)
    api.add_resource(Usuario.Perfil, routes.perfil)
    api.add_resource(Usuario.ObtenerEmail, routes.obtenerEmail)
    api.add_resource(Usuario.GestionarUsuarioEstado, routes.gestionarUsuarioEstado)
    api.add_resource(Usuario.GestionarUsuarioPassword, routes.gestionarUsuarioPassword)
    api.add_resource(Usuario.ResetPasswordResource, routes.resetPassword)
    api.add_resource(Usuario.RequestChangePassword, routes.requestChangePassword)
    api.add_resource(Usuario.BuscarUsuario, routes.buscarUsuario)
    api.add_resource(Usuario.ChangePasswordResource, routes.changePassword)
    api.add_resource(Usuario.ListarPacientes, apiVersion + '/pacientes')
    api.add_resource(Usuario.ListarProgresos, apiVersion + '/progresos')
