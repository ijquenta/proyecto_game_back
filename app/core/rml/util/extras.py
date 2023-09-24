
def getFecha(fecha):
    return fecha if fecha is None else "-".join(fecha.split("T")[0].split("-"))

def getInt(numero):
    pass

def __name(value):
    return value.name

def __getNode(name, parent):
    for i in parent.children:
        if i.name == name:
            return i
def __sumar(acumulado, item):
    acumulado['tmontohb'] += item['tmontohb']
    acumulado['tmontoant'] += item['tmontoant']
    acumulado['tmontolq'] += item['tmontolq']
    return acumulado