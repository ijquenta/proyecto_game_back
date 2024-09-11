from flask import make_response
from core.rml.report_generator import Report
from core.database import select
from utils.date_formatting import *
import pandas as pd

def make(pdf):
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format("archivo.pdf")
    response.mimetype = 'application/pdf'
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte.pdf'
    return response
    
def rptCursoMateriaContabilidad(data):
    params_descuentos = data['descuentos']
    params_resumen = data["resumen"]
    params = select(f'''
                    SELECT 
                    cm.curmatid, cm.curid, c.curnombre, cm.matid, m.matnombre, 
                    cm.periddocente, p.pernomcompleto, p.perfoto, cm.curmatfecini, cm.curmatfecfin, cm.curmatcosto, t1.numest as numero_estudiantes
                    FROM academico.curso_materia cm
                    JOIN ( SELECT curmatid, count(peridestudiante) as numest FROM 
                            academico.inscripcion  WHERE insestado = 1 GROUP BY curmatid
                    ) as t1 ON t1.curmatid = cm.curmatid
                    LEFT JOIN academico.curso c ON c.curid = cm.curid
                    LEFT JOIN academico.materia m ON m.matid = cm.matid
                    left JOIN academico.persona p on p.perid = cm.periddocente
                    WHERE cm.curmatfecini > '{data['fecini']}' AND cm.curmatfecfin < '{data['fecfin']}'
                    and cm.curmatestado = 1
                    ''')
    for p in params:
        p['curmatfecini'] = darFormatoFechaSinHora(p['curmatfecini'])
        p['curmatfecfin'] = darFormatoFechaSinHora(p['curmatfecfin'])   
    return make(Report().RptCursoMateriaContabilidad(params, params_descuentos, params_resumen))

def rptCursoMateriaEstudiante(data):
    user = data['usuname']
    param = select(f'''
        SELECT distinct i.insid, i.matrid, tm.tipmatrgestion, i.curmatid, c.curnombre, c.curfchini, c.curfchfin ,cm.curmatfecini, cm.curmatestado, cm.curmatfecfin, cm.periddocente, p.pernomcompleto, p.pernrodoc, p.perfoto, m2.matnombre, i.peridestudiante, p3.pernomcompleto as pernomcompletoestudiante, p3.pernrodoc as pernrodocestudiante, p3.perfoto as perfotoestudiante, p3.peremail, p3.percelular, p3.pertelefono, i.pagid, i.insusureg, i.insfecreg, 
        i.insusumod, i.insfecmod, i.insestado, i.insestadodescripcion, m.pagoidmatricula, p2.pagmonto, p2.pagestado
        FROM academico.inscripcion i
        left join academico.matricula m on m.matrid = i.matrid 
        left join academico.curso_materia cm on cm.curmatid = i.curmatid 
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        left join academico.persona p on p.perid = cm.periddocente
        left join academico.persona p3 on p3.perid = i.peridestudiante
        left join academico.tipo_matricula tm on tm.tipmatrid = m.tipmatrid
        left join academico.pago p2 on p2.pagid = m.pagoidmatricula
        where i.peridestudiante = {data['perid']}
    ''')
    for p in param:
        p["insfecreg"] = darFormatoFechaConHora(p["insfecreg"])
        p["insfecmod"] = darFormatoFechaConHora(p["insfecmod"])
        p["curmatfecini"] = darFormatoFechaSinHora(p["curmatfecini"])
        p["curmatfecfin"] = darFormatoFechaSinHora(p["curmatfecfin"])
        p["curfchini"] = darFormatoFechaSinHora(p["curfchini"])
        p["curfchfin"] = darFormatoFechaSinHora(p["curfchfin"])

    return make(Report().RptCursoMateriaEstudiante(param, user))


def rptInformacionAdmision(data):
    perid = data['perid']
    usuname = data['usuname']
    
    datos_informacion_personal = select(f'''
        SELECT pip.perid, p.pernomcompleto, p.perfecnac, p.pernrodoc, p.perdirec, te.estadocivilnombre, p.percelular, p.pertelefono, pip.peredad, pip.pernrohijos, pip.perprofesion, tp.pronombre,pip.perfecconversion, pip.perlugconversion, 
        CASE 
            WHEN pip.perbautizoagua IS NOT NULL THEN 'Sí' 
            ELSE 'No' 
        END AS perbautizoagua,
        CASE 
            WHEN pip.perbautizoespiritu IS NOT NULL THEN 'Sí' 
            ELSE 'No' 
        END AS perbautizoespiritu,
        
        pip.pernomiglesia, pip.perdiriglesia, pip.pernompastor, pip.percelpastor,pip.perexperiencia, pip.permotivo, pip.perplanesmetas  
        FROM academico.persona_info_personal pip
        INNER JOIN academico.tipo_profesion tp on tp.proid = pip.perprofesion
        left join academico.persona p on p.perid = pip.perid
        left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil
        WHERE pip.perid = {perid};
    ''')
    if not datos_informacion_personal:
        datos_informacion_personal = [{"pernomcompleto": "", "perdirec": "", "perfecnac": "", "peredad": "", "estadocivilnombre": "", "pernrohijos": "", "pronombre": "", "pernrodoc": "", "perfecconversion": "", "perlugconversion": "", "perbautizoagua": "", "perbautizoespiritu": "", "pertelefono": "", "percelular": "", "pernomiglesia": "", "perdiriglesia": "", "pernompastor": "", "percelpastor": "", "perexperiencia": "", "permotivo":"", "perplanesmetas":""}]
    
    datos_informacion_academica = select(f'''
        SELECT pia.perinfoaca, pia.perid, pia.pereducacion,te.edunombre, pia.pernominstitucion, pia.perdirinstitucion, pia.pergescursadas, pia.perfechas, pia.pertitulo 
        FROM academico.persona_info_academica pia
        JOIN academico.tipo_educacion te on te.eduid = pia.pereducacion
        WHERE perid = {perid}
        order by te.edunombre;
    ''')
    if not datos_informacion_academica:
        datos_informacion_academica = [{"perinfoaca": "", "pereducacion": "", "edunombre": "", "pernominstitucion": "", "perdirinstitucion": "", "pergescursadas": "", "perfechas": "", "pertitulo": ""}]
    
    datos_informacion_ministerial = select(f'''
        SELECT pim.perinfomin, pim.perid, pim.pernomiglesia, pim.percargo,tc.carnombre, pim.pergestion
        FROM academico.persona_info_ministerial pim
        INNER JOIN academico.tipo_cargo tc on tc.carid = pim.percargo
        WHERE perid = {perid}
        order by pim.pernomiglesia;
    ''')
    if not datos_informacion_ministerial:
        datos_informacion_ministerial = [{"perinfomin": "", "perid": "", "pernomiglesia": "", "percargo": "", "carnombre": "", "pergestion": ""}]
    
    datos_documentos_admision = select(f'''
        SELECT 
             perid, 
             CASE 
                 WHEN perfoto IS NOT NULL THEN 'Sí' 
                 ELSE 'No' 
             END AS perfoto,
             CASE 
                 WHEN perfotoci IS NOT NULL THEN 'Sí' 
                 ELSE 'No' 
             END AS perfotoci,
             CASE 
                 WHEN perfototitulo IS NOT NULL THEN 'Sí' 
                 ELSE 'No' 
             END AS perfototitulo,
             CASE 
                 WHEN percartapastor IS NOT NULL THEN 'Sí' 
                 ELSE 'No' 
             END AS percartapastor
         FROM 
             academico.persona_doc_admision
         WHERE 
             perid = {perid};
    ''')
    if not datos_documentos_admision:
        datos_documentos_admision = [{"perid": perid, "perfoto": "No", "perfotoci": "No", "perfototitulo": "No", "percartapastor": "No"}]
    
    try:
        pdf = Report().RptInformacionAdmision(usuname, datos_informacion_personal, datos_informacion_academica, datos_informacion_ministerial, datos_documentos_admision)
        return make(pdf)
    except Exception as e:
        print("Error generating report: ", str(e))
        return {"code": 0, "message": f"Error generating report: {str(e)}"}, 500
    
# Reportes de ejemplo
def rptTotalesSigma():
    params = select(f'''
        SELECT id, nombre_usuario, contrasena, nombre_completo, rol
        FROM public.usuarios;
    ''')
    return make(Report().RptTotalesSigma(params, 1))
"""
def rptBeneficoSocial(idGestion, idMes, codDocente, nroLiquidacion):
    params = select(f'''
        SELECT *
        FROM p_bsocial.bs_reporte_indemnizacion_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}')
        AS (ano integer,mes integer,cod_docente varchar,nom_completo varchar, nro_ci varchar, lug_ci varchar, ano_ingreso integer, mes_ingreso integer, dia_ingreso integer, nro_liquidacion varchar, fec_liquidacion date, nro_dictamen varchar, hoja_ruta varchar, tipo_motivo varchar,
            items varchar, ch varchar, ano_retiro integer, mes_retiro integer, dia_retiro integer, ts_ano smallint, ts_mes smallint, ts_dia smallint,
            facultad varchar, carreras varchar, cargo varchar, categoria varchar, deducciones varchar, monto_desahucio numeric, monto_tindemnizacion numeric, monto_tgeneral numeric, monto_tdeducciones numeric, monto_tliquido_pagable numeric,
            monto_cfiscal numeric, ssu_gestion1 smallint, ssu_gestion2 smallint, ssu_gestion3 smallint, monto_ssu1 numeric, monto_ssu2 numeric, monto_ssu3 numeric, monto_tssu numeric);
    ''')
    params2 = select(f''' SELECT * FROM p_bsocial.bs_reporte_remuneraciones_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}') AS (desc_mes varchar, tg_dias integer, monto_tganado numeric, factor_ipc numeric, tganado_actualizado numeric, descripcion varchar, promedio numeric); ''')
    params3 = select(f''' SELECT * FROM p_bsocial.bs_reporte_benef_tipos_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}') AS (orden integer, descripcion varchar, cantidad text, monto text, total text) order by orden ;  ''')
    params4 = select(f''' select * from p_bsocial.t_beneficio_firma tbf where estado = 1 ''')
    return make(Report().RptBeneficioSocial(params, params2, params3, params4, 1, idGestion, 1))

def rptReintegroBeneficoSocial(idGestion, idMes, codDocente, nroLiquidacion):
    params = select(f'''
        SELECT *
        FROM p_bsocial.bs_reporte_indemnizacion_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}')
        AS (ano integer,mes integer,cod_docente varchar,nom_completo varchar, nro_ci varchar, lug_ci varchar, ano_ingreso integer, mes_ingreso integer, dia_ingreso integer, nro_liquidacion varchar, fec_liquidacion date, nro_dictamen varchar, hoja_ruta varchar, tipo_motivo varchar,
            items varchar, ch varchar, ano_retiro integer, mes_retiro integer, dia_retiro integer, ts_ano smallint, ts_mes smallint, ts_dia smallint,
            facultad varchar, carreras varchar, cargo varchar, categoria varchar, deducciones varchar, monto_desahucio numeric, monto_tindemnizacion numeric, monto_tgeneral numeric, monto_tdeducciones numeric, monto_tliquido_pagable numeric,
            monto_cfiscal numeric, ssu_gestion1 smallint, ssu_gestion2 smallint, ssu_gestion3 smallint, monto_ssu1 numeric, monto_ssu2 numeric, monto_ssu3 numeric, monto_tssu numeric);
    ''')
    params2 = select(f''' SELECT * FROM p_bsocial.bs_reporte_remuneraciones_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}') AS (desc_mes varchar, tg_dias integer, monto_tganado numeric, factor_ipc numeric, tganado_actualizado numeric, descripcion varchar, promedio numeric); ''')
    params3 = select(f''' SELECT * FROM p_bsocial.rei_reporte_benef_tipos_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}') AS (orden integer, descripcion varchar, cantidad text, monto text,monto_des text,monto_rei text, total text) order by orden ;;  ''')
    params4 = select(f''' select * from p_bsocial.t_beneficio_firma tbf where estado = 1 ''')
    return make(Report().RptReintegroBeneficioSocial(params, params2, params3, params4, 1, idGestion, 1))


def rptConsolidadoBeneficoSocial(idGestion, idMes, codDocente, nroLiquidacion):
    params = select(f'''
        SELECT *
        FROM p_bsocial.bs_reporte_indemnizacion_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}')
        AS (ano integer,mes integer,cod_docente varchar,nom_completo varchar, nro_ci varchar, lug_ci varchar, ano_ingreso integer, mes_ingreso integer, dia_ingreso integer, nro_liquidacion varchar, fec_liquidacion date, nro_dictamen varchar, hoja_ruta varchar, tipo_motivo varchar,
            items varchar, ch varchar, ano_retiro integer, mes_retiro integer, dia_retiro integer, ts_ano smallint, ts_mes smallint, ts_dia smallint,
            facultad varchar, carreras varchar, cargo varchar, categoria varchar, deducciones varchar, monto_desahucio numeric, monto_tindemnizacion numeric, monto_tgeneral numeric, monto_tdeducciones numeric, monto_tliquido_pagable numeric,
            monto_cfiscal numeric, ssu_gestion1 smallint, ssu_gestion2 smallint, ssu_gestion3 smallint, monto_ssu1 numeric, monto_ssu2 numeric, monto_ssu3 numeric, monto_tssu numeric);
    ''')
    params2 = select(f''' SELECT * FROM p_bsocial.bs_reporte_remuneraciones_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}') AS (desc_mes varchar, tg_dias integer, monto_tganado numeric, factor_ipc numeric, tganado_actualizado numeric, descripcion varchar, promedio numeric); ''')
    params3 = select(f''' SELECT * FROM p_bsocial.bs_reporte_benef_tipos_docente({idGestion},{idMes}, '{codDocente}','{nroLiquidacion}') AS (orden integer, descripcion varchar, cantidad text, monto text, total text) order by orden ;  ''')
    params4 = select(f''' select * from p_bsocial.t_beneficio_firma tbf where estado = 1 ''')
    return make(Report().RptConsolidadoBeneficioSocial(params, params2, params3, params4, 1, idGestion, 1))
"""