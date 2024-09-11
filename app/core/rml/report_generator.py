# Manipulación de plantillas preppy para generar informes, documentos, etc.
import preppy
from io import BytesIO  # Operaciones con datos en memoria como archivos binarios
# Generación de archivos PDF a partir de datos usando RML
from core.rml.util.to_pdf import generatePdf

# Ruta de los repotes .prep
PATH = 'core/rml/templates/'


class Report():

    def RptInformacionAdmision(self, usuname, data1, data2, data3, data4):
        try:
            templateTs = preppy.getModule(PATH+'rptInformacionAdmision.prep')
            with BytesIO(bytes(templateTs.get(usuname, data1, data2, data3, data4), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt InformacionAdmision: ", e)

    def RptCursoMateriaContabilidad(self, data, data2, data3):
        try:
            templateTs = preppy.getModule(
                PATH+'rptCursoMateriaContabilidad.prep')
            with BytesIO(bytes(templateTs.get(data, data2, data3), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt CursoMateriaContabilidad: ", e)
            
    def RptCursoMateriaEstudiante(self, data, user):
        try:
            templateTS = preppy.getModule(PATH+'rptCursoMateriaEstudiante.prep')
            with BytesIO(bytes(templateTS.get(data, user), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt CursoMateriaEstudiante: ", e)

    def RptNotaEstudianteMateria(self, cursos, estudiante, usuname, resumen):
        try:
            templateTS = preppy.getModule(PATH+'rptNotaEstudianteMateria.prep')
            with BytesIO(bytes(templateTS.get(cursos, estudiante, usuname, resumen), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaEstudianteMateria: ", e)
            
    def RptPagoEstudianteMateria(self, cursos, estudiante, usuname):
        try:
            templateTS = preppy.getModule(PATH+'rptPagoEstudianteMateria.prep')
            with BytesIO(bytes(templateTS.get(cursos, estudiante, usuname), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt PagoEstudianteMateria: ", e)
            
    def GenerarComprobantePagoPDF(self, comprobante, usuname):
        try:
            templateTS = preppy.getModule(PATH+'generarComprobantePagoPDF.prep')
            with BytesIO(bytes(templateTS.get(comprobante, usuname), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt generarComprobantePagoPDF: ", e)
            
    
    def GenerarComprobantePagoMatriculaPDF(self, comprobante, usuname):
     try:
         templateTS = preppy.getModule(PATH+'generarComprobantePagoMatriculaPDF.prep')
         with BytesIO(bytes(templateTS.get(comprobante, usuname), 'utf-8')) as buffer:
             with BytesIO() as output:
                 generatePdf(buffer, output)
                 pdf_out = output.getvalue()
         return pdf_out
     except Exception as e:
         print("Error rpt generarComprobantePagoPDF: ", e)

    def RptNotaCursoMateria(self, data, user):
        try:
            templateTS = preppy.getModule(PATH+'rptNotaCursoMateria.prep')
            with BytesIO(bytes(templateTS.get(data, user), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaCursoMateria: ", e)

    def RptNotaCursoMateriaGeneral(self, data, user):
        try:
            templateTS = preppy.getModule(
                PATH+'rptNotaCursoMateriaGeneral.prep')
            with BytesIO(bytes(templateTS.get(data, user), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaCursoMateriaGeneral", e)

    def RptNotaCursoMateriaDocente(self, data, user):
        try:
            templateTS = preppy.getModule(
                PATH+'rptNotaCursoMateriaDocente.prep')
            with BytesIO(bytes(templateTS.get(data, user), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaCursoMateriaDocente", e)

