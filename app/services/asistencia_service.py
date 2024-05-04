from core.database import select, as_string, execute, execute_function, execute_response

def listarAsistencia():
    return select('''
        SELECT asisid, insid, asifecha, asidescripcion, asiusureg, asifecreg, asiusumod, asifecmod, asiestado FROM academico.asistencia;
    ''')