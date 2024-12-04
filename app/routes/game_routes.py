from flask_restful import Api
<<<<<<< HEAD
import resources.Game as Game
apiVersion = "/v1"

def game_routes(api: Api):
    api.add_resource(Game.ObtenerUsuarios, apiVersion + '/usuarios')
    api.add_resource(Game.ObtenerPacientes, apiVersion + '/pacientes')
    api.add_resource(Game.ObtenerDoctores, apiVersion + '/doctores')
    api.add_resource(Game.ObtenerSesiones, apiVersion + '/sesiones')
    
    api.add_resource(Game.CrearUsuario, apiVersion + '/usuarios')
    api.add_resource(Game.CrearPaciente, apiVersion + '/pacientes')
    api.add_resource(Game.CrearDoctor, apiVersion + '/doctores')
    api.add_resource(Game.CrearSesion, apiVersion + '/sesiones')
    
    api.add_resource(Game.ModificarUsuario, apiVersion + '/usuarios/<int:usuario_id>')
    api.add_resource(Game.ModificarPaciente, apiVersion + '/pacientes/<int:paciente_id>')
    api.add_resource(Game.ModificarDoctor, apiVersion + '/doctores/<int:doctor_id>')
    api.add_resource(Game.ModificarSesion, apiVersion + '/sesiones/<int:sesion_id>')
    
    api.add_resource(Game.DesactivarDoctor, apiVersion + '/usuarios/<int:usuario_id>')
    api.add_resource(Game.DesactivarPaciente, apiVersion + '/pacientes/<int:paciente_id>')
    api.add_resource(Game.DesactivarUsuario, apiVersion + '/doctores/<int:doctor_id>')
    api.add_resource(Game.DesactivarSesion, apiVersion + '/sesiones/<int:sesion_id>')
=======
import resources.game_resource as Persona
import resources.game_resource as Usuario

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
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
