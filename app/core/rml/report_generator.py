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