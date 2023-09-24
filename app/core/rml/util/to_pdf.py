from lxml import etree
import os
import sys
from z3c.rml import document

def generatePdf(xmlInputName, outputFileName=None, outDir=None, dtdDir=None):
    if dtdDir is not None:
        sys.stderr.write('The ``dtdDir`` option is not yet supported.\n')

    if hasattr(xmlInputName, 'read'):
        # it is already a file-like object
        xmlFile = xmlInputName
        xmlInputName = 'input.pdf'
    else:
        xmlFile = open(xmlInputName, 'rb')
    root = etree.parse(xmlFile).getroot()
    doc = document.Document(root)
    doc.filename = xmlInputName

    outputFile = None

    # If an output filename is specified, create an output filepointer for it
    if outputFileName is not None:
        if hasattr(outputFileName, 'write'):
            # it is already a file-like object
            outputFile = outputFileName
            outputFileName = 'output.pdf'
        else:
            if outDir is not None:
                outputFileName = os.path.join(outDir, outputFileName)
            outputFile = open(outputFileName, 'wb')

    # Create a Reportlab canvas by processing the document
    try:
        doc.process(outputFile)
    finally:
        xmlFile.close()