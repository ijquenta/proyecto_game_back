import preppy
from io import BytesIO
from core.rml.util.to_pdf import generatePdf

PATH = 'core/rml/templates/'
class Report():    
    def RptHaberesDescuentos(self, data, partida, idGestion, user):
        template = preppy.getModule(PATH+'rptHaberesDescuentos.prep')
        # print(data)
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
    
    def RptTotalesSigma(self, data, user):
        # print("report -----------")
        # print(data)
        # print("--->>>>>>>>")
        # print(PATH)
        templateTS = preppy.getModule(PATH+'rptTotalesSigma.prep')        
        with BytesIO(bytes(templateTS.get(data, user),'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue()
        # print('Enviandos archivo rptTotalSimga')
        return pdf_out
    
    def RptCursoMateriaContabilidad(self, data, data2, data3):
        # print("Reporte Curso Materia Contabilidad: ", data)
        templateTs = preppy.getModule(PATH+'rptCursoMateriaContabilidad.prep')
        with BytesIO(bytes(templateTs.get(data, data2, data3), 'utf-8')) as buffer:
            with BytesIO() as output:
                generatePdf(buffer, output)
                pdf_out = output.getvalue()
        return pdf_out
    
    def RptNotaEstudianteMateria(self, data, user):    
        try:
            print("Entrando en la función RptNotaEstudianteMateria")
            print("datos", data)
            print("PATCH: ",PATH)
            templateTS = preppy.getModule(PATH+'rptNotaEstudianteMateria.prep')        
            with BytesIO(bytes(templateTS.get(data, user),'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            print('Enviandos archivo rptNotaEstudianteMateria')
            return pdf_out
            # Resto del código...
        except Exception as e:
            print("Error en la función RptNotaEstudianteMateria:", e)
            # Manejar el error de alguna manera
       
    
    def RptNotaCursoMateria(self, data, user):
        try:
            print("Entrando en la función RptNotaCursoMateria")
            print("datos", data)
            print("PATCH: ", PATH   )
            templateTS = preppy.getModule(PATH+'rptNotaCursoMateria.prep')        
            with BytesIO(bytes(templateTS.get(data, user),'utf-8')) as buffer:
                with BytesIO() as output:
                    generatePdf(buffer, output)
                    pdf_out = output.getvalue()
            print('Enviado archivo rptNotaCursoMateria')
            return pdf_out
        except Exception as e:
            print("Error en la función RptNotaCursoMateria:", e)
            # Manejar el error de alguna manera
       