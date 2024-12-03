from core.database import select

def listarAsistencia():
    return select('''
        SELECT asisid, insid, asifecha, asidescripcion, asiusureg, asifecreg, asiusumod, asifecmod, asiestado FROM academico.asistencia;
    ''')