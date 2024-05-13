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
