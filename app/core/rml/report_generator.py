import preppy  # Manipulación de plantillas preppy para generar informes, documentos, etc.
from io import BytesIO  # Operaciones con datos en memoria como archivos binarios
from core.rml.util.to_pdf import generatePdf  # Generación de archivos PDF a partir de datos usando RML

# Ruta de los repotes .prep
PATH = 'core/rml/templates/'
class Report():    
   
    def RptCursoMateriaContabilidad(self, data, data2, data3):
        try:
            templateTs = preppy.getModule(PATH+'rptCursoMateriaContabilidad.prep')
            with BytesIO(bytes(templateTs.get(data, data2, data3), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt CursoMateriaContabilidad: ", e)
    
    def RptNotaEstudianteMateria(self, data, user):    
        try:
            templateTS = preppy.getModule(PATH+'rptNotaEstudianteMateria.prep')        
            with BytesIO(bytes(templateTS.get(data, user),'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaEstudianteMateria: ", e)
       
    def RptNotaCursoMateria(self, data, user):
        try:
            templateTS = preppy.getModule(PATH+'rptNotaCursoMateria.prep')        
            with BytesIO(bytes(templateTS.get(data, user),'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaCursoMateria: ", e)
            
    def RptNotaCursoMateriaGeneral(self, data, user):
        try:
            templateTS = preppy.getModule(PATH+'rptNotaCursoMateriaGeneral.prep')
            with BytesIO(bytes(templateTS.get(data, user), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaCursoMateriaGeneral", e)
            
    def RptNotaCursoMateriaDocente(self, data, user):
        try:
            templateTS = preppy.getModule(PATH+'rptNotaCursoMateriaDocente.prep')
            with BytesIO(bytes(templateTS.get(data, user), 'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            return pdf_out
        except Exception as e:
            print("Error rpt NotaCursoMateriaDocente", e)
        
    
    def RptTotalesSigma(self, data, user):
        templateTS = preppy.getModule(PATH+'rptTotalesSigma.prep')        
        with BytesIO(bytes(templateTS.get(data, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue()
        return pdf_out






# Reportes de ejemplo

"""
 def RptHaberesDescuentos(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptHaberesDescuentos.prep')
        with BytesIO(bytes(template.get(data, idGestion, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue() 
        print('enviando archivo rptHaberesDescuentos')
        return pdf_out

    def RptHaberesBorrador(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptHaberesBorrador.prep')
        # print(data)
        with BytesIO(bytes(template.get(data, idGestion, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue() 
        print('enviando archivo rptHaberesBorrador')
        return pdf_out

    def RptHaberesResumen(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptHaberesResumen.prep')
        with BytesIO(bytes(template.get(data, idGestion, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue() 
        print('enviando archivo rptHaberesResumen')
        return pdf_out
    
    def RptHaberesExAdministrativos(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptHaberesDescuentos.prep')
        # print(data)
        with BytesIO(bytes(template.get(data, idGestion, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue() 
        print('enviando archivo rptHaberesDescuentosExAdm')
        return pdf_out
    
    def RptHaberesResumenExAdministrativos(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptHaberesResumen.prep')
        with BytesIO(bytes(template.get(data, idGestion, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue() 
        print('enviando archivo rptHaberesResumenExAdm')
        return pdf_out

    def RptPersonalExcluido(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptPersonalExcluido.prep')
        with BytesIO(bytes(template.get(data, idGestion, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue() 
        print('enviando archivo rptPersonalExcluido')
        return pdf_out
    
    def RptHaberesAportes(self, data, entidades, partida, idGestion, idMes, user):
        template = preppy.getModule(PATH+'rptHaberesAportes.prep')
        with BytesIO(bytes(template.get(data, entidades, idGestion, idMes, partida, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue()         
        print(f'enviando archivo rptHaberesAportes - {idMes}')
        return pdf_out
"""