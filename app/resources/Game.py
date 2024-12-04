from flask_restful import Resource, reqparse

from services.game_service import *

class ObtenerUsuarios(Resource):
    def get(self):
        return obtenerUsuarios()
    
class ObtenerPacientes(Resource):
    def get(self):
        return obtenerPacientes()
    
class ObtenerDoctores(Resource):
    def get(self):
        return obtenerDoctores()
    
class ObtenerSesiones(Resource):
    def get(self):
        return obtenerSesiones()
    
class ObtenerUsuarioPorId(Resource):
    def get(self, usuario_id):
        return obtenerUsuarioPorId(usuario_id)


# Parsers para Usuario
parseCreateUsuario = reqparse.RequestParser()
parseCreateUsuario.add_argument('nombre', type=str, required=True, help='Ingrese el nombre')
parseCreateUsuario.add_argument('apellido', type=str, required=True, help='Ingrese el apellido')
parseCreateUsuario.add_argument('email', type=str, required=True, help='Ingrese el email')
parseCreateUsuario.add_argument('numero_carnet', type=str, required=True, help='Ingrese el número de carnet')
parseCreateUsuario.add_argument('telefono', type=str, required=True, help='Ingrese el teléfono')
parseCreateUsuario.add_argument('fecha_nacimiento', type=str, help='Ingrese la fecha de nacimiento (YYYY-MM-DD)')
parseCreateUsuario.add_argument('rol', type=str, required=True, help='Ingrese el rol')

parseUpdateUsuario = reqparse.RequestParser()
parseUpdateUsuario.add_argument('nombre', type=str, help='Ingrese el nombre')
parseUpdateUsuario.add_argument('apellido', type=str, help='Ingrese el apellido')
parseUpdateUsuario.add_argument('email', type=str, help='Ingrese el email')
parseUpdateUsuario.add_argument('numero_carnet', type=str, help='Ingrese el número de carnet')
parseUpdateUsuario.add_argument('telefono', type=str, help='Ingrese el teléfono')
parseUpdateUsuario.add_argument('fecha_nacimiento', type=str, help='Ingrese la fecha de nacimiento (YYYY-MM-DD)')
parseUpdateUsuario.add_argument('rol', type=str, help='Ingrese el rol')


# Parsers para Paciente
parseCreatePaciente = reqparse.RequestParser()
parseCreatePaciente.add_argument('id_usuario', type=int, required=True, help='Ingrese el ID del usuario')
parseCreatePaciente.add_argument('diagnostico', type=str)
parseCreatePaciente.add_argument('rango_movimiento', type=str)
parseCreatePaciente.add_argument('fuerza', type=str)
parseCreatePaciente.add_argument('estabilidad', type=str)
parseCreatePaciente.add_argument('descripcion', type=str)
parseCreatePaciente.add_argument('observacion', type=str)

parseUpdatePaciente = reqparse.RequestParser()
parseUpdatePaciente.add_argument('diagnostico', type=str, help='Ingrese el diagnóstico')
parseUpdatePaciente.add_argument('rango_movimiento', type=str, help='Ingrese el rango de movimiento')
parseUpdatePaciente.add_argument('fuerza', type=str, help='Ingrese la fuerza')
parseUpdatePaciente.add_argument('estabilidad', type=str, help='Ingrese la estabilidad')
parseUpdatePaciente.add_argument('descripcion', type=str, help='Ingrese la descripción')
parseUpdatePaciente.add_argument('observacion', type=str, help='Ingrese la observación')

# Parsers para Doctor
parseCreateDoctor = reqparse.RequestParser()
parseCreateDoctor.add_argument('id_usuario', type=int, required=True, help='Ingrese el ID del usuario')
parseCreateDoctor.add_argument('especialidad', type=str)

parseUpdateDoctor = reqparse.RequestParser()
parseUpdateDoctor.add_argument('especialidad', type=str, help='Ingrese la especialidad')

# Parsers para Sesion
parseCreateSesion = reqparse.RequestParser()
parseCreateSesion.add_argument('id_paciente', type=int, required=True, help='Ingrese el ID del paciente')
parseCreateSesion.add_argument('id_doctor', type=int, required=True, help='Ingrese el ID del doctor')
parseCreateSesion.add_argument('tiempo_sesion', type=int)
parseCreateSesion.add_argument('puntaje_obtenido', type=int)
parseCreateSesion.add_argument('descripcion', type=str)
parseCreateSesion.add_argument('observaciones', type=str)
parseCreateSesion.add_argument('ejercicios_realizados', type=str)
parseCreateSesion.add_argument('nivel_dificultad', type=str, required=True, help='Ingrese el nivel de dificultad')
parseCreateSesion.add_argument('estado_emocional', type=str, required=True, help='Ingrese el estado emocional')

parseUpdateSesion = reqparse.RequestParser()
parseUpdateSesion.add_argument('tiempo_sesion', type=int, help='Ingrese el tiempo de la sesión')
parseUpdateSesion.add_argument('puntaje_obtenido', type=int, help='Ingrese el puntaje obtenido')
parseUpdateSesion.add_argument('descripcion', type=str, help='Ingrese la descripción')
parseUpdateSesion.add_argument('observaciones', type=str, help='Ingrese las observaciones')
parseUpdateSesion.add_argument('ejercicios_realizados', type=str, help='Ingrese los ejercicios realizados')
parseUpdateSesion.add_argument('nivel_dificultad', type=str, help='Ingrese el nivel de dificultad')
parseUpdateSesion.add_argument('estado_emocional', type=str, help='Ingrese el estado emocional')


class CrearUsuario(Resource):
    def post(self):
        data = parseCreateUsuario.parse_args()
        return crearUsuario(data)

class CrearPaciente(Resource):
    def post(self):
        data = parseCreatePaciente.parse_args()
        return crearPaciente(data)

class CrearDoctor(Resource):
    def post(self):
        data = parseCreateDoctor.parse_args()
        return crearDoctor(data)

class CrearSesion(Resource):
    def post(self):
        data = parseCreateSesion.parse_args()
        return crearSesion(data)

# Parsers para actualización de Usuario

class ModificarUsuario(Resource):
    def put(self, usuario_id):
        data = parseUpdateUsuario.parse_args()
        return modificarUsuario(data, usuario_id)

class ModificarPaciente(Resource):
    def put(self, paciente_id):
        data = parseUpdatePaciente.parse_args()
        return modificarPaciente(data, paciente_id)

class ModificarDoctor(Resource):
    def put(self, doctor_id):
        data = parseUpdateDoctor.parse_args()
        return modificarDoctor(data, doctor_id)

class ModificarSesion(Resource):
    def put(self, sesion_id):
        data = parseUpdateSesion.parse_args()
        return modificarSesion(data, sesion_id)




# Clases de recursos para desactivar Usuario
class DesactivarUsuario(Resource):
    def delete(self, usuario_id):
        return desactivarUsuario(usuario_id)

# Clases de recursos para desactivar Paciente
class DesactivarPaciente(Resource):
    def delete(self, paciente_id):
        return desactivarPaciente(paciente_id)

# Clases de recursos para desactivar Doctor
class DesactivarDoctor(Resource):
    def delete(self, doctor_id):
        return desactivarDoctor(doctor_id)

# Clases de recursos para desactivar Sesion
class DesactivarSesion(Resource):
    def delete(self, sesion_id):
        return desactivarSesion(sesion_id)