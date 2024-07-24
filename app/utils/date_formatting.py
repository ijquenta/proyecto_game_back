from datetime import datetime

"""
    Funciónes para dar formatado a los datos de retorna al frotend
"""

def darFormatoFechaConHora(fecha_str):
    if fecha_str is None:
       return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_formateada

def darFormatoFechaSinHora(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
    return fecha_formateada

def darFormatoFechaSinHorav2(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%Y-%m-%d")
    return fecha_formateada


def darFormatoFechaNacimiento(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
    return fecha_formateada 

def darFormatoFechaNacimientov2(fecha_str):
    if not fecha_str:   
        return None

    # Lista de formatos posibles
    formatos_posibles = [
        "%a %b %d %Y %H:%M:%S GMT%z (hora de Bolivia)",
        "%Y-%m-%d",  # Formato '1999-01-30'
        "%Y-%m-%dT%H:%M:%S.%fZ",  # Formato '2023-07-03T20:01:12.881757Z'
        "%Y-%m-%d %H:%M:%S"  # Formato '2023-07-03 20:01:12'
    ]

    for formato in formatos_posibles:
        try:
            # Intentar convertir la fecha utilizando el formato actual
            fecha_datetime = datetime.strptime(fecha_str, formato)
            # Formatear la fecha en el formato deseado
            fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
            return fecha_formateada
        except ValueError:
            # Si ocurre un ValueError, continuar con el siguiente formato
            continue

    # Si ningún formato coincide, retornar None o lanzar una excepción
    return None

def darFormatoFechaSinHoraAlReves(fecha_str):
    if not fecha_str:
        return None
    fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_formateada = fecha_datetime.strftime("%Y-%m-%d")
    return fecha_formateada

def volverAFormatoOriginal(fecha_str):
    if not fecha_str:
        return None
    
    # Verificar si la fecha ya está en el formato deseado
    if "T" in fecha_str and "Z" in fecha_str:
        return fecha_str
    
    fecha_datetime = datetime.strptime(fecha_str, "%d/%m/%Y")
    fecha_formateada = fecha_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return fecha_formateada


def formatDateBirth(fecha_str):
    if not fecha_str:   
        return None

    # Lista de formatos posibles
    formatos_posibles = [
        "%a %b %d %Y %H:%M:%S GMT%z (hora de Bolivia)",
        "%Y-%m-%d",  # Formato '1999-01-30'
        "%Y-%m-%dT%H:%M:%S.%fZ",  # Formato '2023-07-03T20:01:12.881757Z'
        "%Y-%m-%d %H:%M:%S"  # Formato '2023-07-03 20:01:12'
    ]

    for formato in formatos_posibles:
        try:
            # Intentar convertir la fecha utilizando el formato actual
            fecha_datetime = datetime.strptime(fecha_str, formato)
            # Formatear la fecha en el formato deseado
            fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
            return fecha_formateada
        except ValueError:
            # Si ocurre un ValueError, continuar con el siguiente formato
            continue

    # Si ningún formato coincide, retornar None o lanzar una excepción
    return None