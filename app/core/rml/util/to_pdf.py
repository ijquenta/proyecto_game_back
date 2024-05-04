from lxml import etree  # Manipulación de documentos XML y HTML de forma eficiente
import os  # Operaciones con el sistema operativo, como manipulación de archivos y directorios
import sys  # Interacción con el intérprete de Python y el sistema operativo
from z3c.rml import document  # Creación y manipulación de documentos RML (Report Markup Language)

# Función para generar el documento PDF
def generatePdf(xmlInputName, outputFileName=None, outDir=None, dtdDir=None):
    # Comprueba si la opción `dtdDir` está presente y emite un mensaje de advertencia si lo está
    if dtdDir is not None:
        sys.stderr.write('The ``dtdDir`` option is not yet supported.\n')

    # Verifica si `xmlInputName` es un archivo abierto o un nombre de archivo y ajusta en consecuencia
    if hasattr(xmlInputName, 'read'):
        xmlFile = xmlInputName  # Si es un archivo abierto, se asigna directamente
        xmlInputName = 'input.pdf'  # Se cambia el nombre de entrada a 'input.pdf'
    else:
        xmlFile = open(xmlInputName, 'rb')  # Si es un nombre de archivo, se abre en modo lectura binaria

    # Parsea el archivo XML y obtiene el elemento raíz
    root = etree.parse(xmlFile).getroot()
    
    # Crea un objeto `Document` de RML a partir del elemento raíz XML
    doc = document.Document(root)
    doc.filename = xmlInputName  # Asigna el nombre del archivo de entrada al atributo `filename` del objeto `Document`

    outputFile = None  # Inicializa la variable `outputFile` a `None`

    # Verifica si se ha especificado un nombre de archivo de salida
    if outputFileName is not None:
        # Comprueba si `outputFileName` es un archivo abierto o un nombre de archivo y ajusta en consecuencia
        if hasattr(outputFileName, 'write'):
            outputFile = outputFileName  # Si es un archivo abierto, se asigna directamente
            outputFileName = 'output.pdf'  # Se cambia el nombre de salida a 'output.pdf'
        else:
            # Si es un nombre de archivo, se verifica si se ha especificado un directorio de salida y se ajusta en consecuencia
            if outDir is not None:
                outputFileName = os.path.join(outDir, outputFileName)
            outputFile = open(outputFileName, 'wb')  # Se abre el archivo de salida en modo escritura binaria

    # Crea un documento PDF procesando el objeto `Document`
    try:
        doc.process(outputFile)
    finally:
        xmlFile.close()  # Cierra el archivo XML al finalizar
