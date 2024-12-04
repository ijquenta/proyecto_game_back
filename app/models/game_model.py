from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
<<<<<<< HEAD
    __table_args__ = {'schema': 'game'}
=======
    __table_args__ = {'schema': 'game'} 
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3

    id_usuario = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Text, nullable=False)
    apellido = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    numero_carnet = db.Column(db.Text, nullable=False, unique=True)
    telefono = db.Column(db.Text, nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    rol = db.Column(db.Text, nullable=False)
<<<<<<< HEAD
    fecha_creacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
=======
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
    estado = db.Column(db.Text, default='activo')

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'numero_carnet': self.numero_carnet,
            'telefono': self.telefono,
            'fecha_nacimiento': self.fecha_nacimiento,
            'rol': self.rol,
            'fecha_creacion': self.fecha_creacion,
<<<<<<< HEAD
            'estado': self.estado
        }
=======
            'estado': self.estado,
        }
    
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    __table_args__ = {'schema': 'game'}

    id_paciente = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
<<<<<<< HEAD
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('game.usuarios.id_usuario'), nullable=False)
    diagnostico = db.Column(db.Text)
    fecha_ingreso = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
=======
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('game.usuarios.id_usuario'), nullable=False)  # FK a Usuario
    diagnostico = db.Column(db.Text)
    fecha_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
    rango_movimiento = db.Column(db.Text)
    fuerza = db.Column(db.Text)
    estabilidad = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    observacion = db.Column(db.Text)
<<<<<<< HEAD
    estado = db.Column(db.Text, default='activo')
=======
    estado = db.Column(db.Text, default='activo')  # 'activo', 'inactivo'
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3

    usuario = db.relationship('Usuario', backref='pacientes')

    def to_dict(self):
        return {
            'id_paciente': self.id_paciente,
            'id_usuario': self.id_usuario,
            'diagnostico': self.diagnostico,
            'fecha_ingreso': self.fecha_ingreso,
            'rango_movimiento': self.rango_movimiento,
            'fuerza': self.fuerza,
            'estabilidad': self.estabilidad,
            'descripcion': self.descripcion,
            'observacion': self.observacion,
<<<<<<< HEAD
            'estado': self.estado
        }

=======
            'estado': self.estado,
        }
    
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
class Doctor(db.Model):
    __tablename__ = 'doctores'
    __table_args__ = {'schema': 'game'}

    id_doctor = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
<<<<<<< HEAD
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('game.usuarios.id_usuario'), nullable=False)
    especialidad = db.Column(db.Text)
    estado = db.Column(db.Text, default='activo')
=======
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('game.usuarios.id_usuario'), nullable=False)  # FK a Usuario
    especialidad = db.Column(db.Text)
    estado = db.Column(db.Text, default='activo')  # 'activo', 'inactivo'

>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
    usuario = db.relationship('Usuario', backref='doctores')

    def to_dict(self):
        return {
            'id_doctor': self.id_doctor,
            'id_usuario': self.id_usuario,
            'especialidad': self.especialidad,
<<<<<<< HEAD
            'estado': self.estado
        }

=======
            'estado': self.estado,
        }
    
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
class Administrador(db.Model):
    __tablename__ = 'administradores'
    __table_args__ = {'schema': 'game'}

    id_administrador = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
<<<<<<< HEAD
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('game.usuarios.id_usuario'), nullable=False)
    estado = db.Column(db.Text, default='activo')
=======
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('game.usuarios.id_usuario'), nullable=False)  # FK a Usuario
    estado = db.Column(db.Text, default='activo')  # 'activo', 'inactivo'
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3

    usuario = db.relationship('Usuario', backref='administradores')

    def to_dict(self):
        return {
            'id_administrador': self.id_administrador,
            'id_usuario': self.id_usuario,
<<<<<<< HEAD
            'estado ': self.estado
=======
            'estado': self.estado,
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
        }
    
class Sesion(db.Model):
    __tablename__ = 'sesiones'
    __table_args__ = {'schema': 'game'}

    id_session = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
<<<<<<< HEAD
    id_paciente = db.Column(db.BigInteger, db.ForeignKey('game.pacientes.id_paciente'), nullable=False)
    id_doctor = db.Column(db.BigInteger, db.ForeignKey('game.doctores.id_doctor'), nullable=False)
    fecha_sesion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    tiempo_sesion = db.Column(db.Integer)
=======
    id_paciente = db.Column(db.BigInteger, db.ForeignKey('game.pacientes.id_paciente'), nullable=False)  # FK a Paciente
    id_doctor = db.Column(db.BigInteger, db.ForeignKey('game.doctores.id_doctor'), nullable=False)  # FK a Doctor
    fecha_sesion = db.Column(db.DateTime, default=db.func.current_timestamp())
    tiempo_sesion = db.Column(db.Integer)  # En minutos
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
    puntaje_obtenido = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    ejercicios_realizados = db.Column(db.Text)
<<<<<<< HEAD
    nivel_dificultad = db.Column(db.Text, nullable=False)
    estado_emocional = db.Column(db.Text, nullable=False)
=======
    nivel_dificultad = db.Column(db.Text)  # 'bajo', 'medio', 'alto'
    estado_emocional = db.Column(db.Text)  # 'bueno', 'regular', 'malo'
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
    mejoras_observadas = db.Column(db.Text)
    resultados_prueba = db.Column(db.Text)
    notas = db.Column(db.Text)
    feedback = db.Column(db.Text)
<<<<<<< HEAD
    estado = db.Column(db.Text, default='activo')
=======
    estado = db.Column(db.Text, default='activo')  # 'activo', 'inactivo'
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3

    paciente = db.relationship('Paciente', backref='sesiones')
    doctor = db.relationship('Doctor', backref='sesiones')

    def to_dict(self):
        return {
            'id_session': self.id_session,
            'id_paciente': self.id_paciente,
            'id_doctor': self.id_doctor,
            'fecha_sesion': self.fecha_sesion,
            'tiempo_sesion': self.tiempo_sesion,
            'puntaje_obtenido': self.puntaje_obtenido,
            'descripcion': self.descripcion,
            'observaciones': self.observaciones,
            'ejercicios_realizados': self.ejercicios_realizados,
            'nivel_dificultad': self.nivel_dificultad,
            'estado_emocional': self.estado_emocional,
            'mejoras_observadas': self.mejoras_observadas,
            'resultados_prueba': self.resultados_prueba,
            'notas': self.notas,
            'feedback': self.feedback,
<<<<<<< HEAD
            'estado': self.estado
=======
            'estado': self.estado,
>>>>>>> b3fdec4d0ac3029801254df316279e2aaddd7bc3
        }