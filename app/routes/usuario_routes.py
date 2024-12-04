from flask_restful import Api
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