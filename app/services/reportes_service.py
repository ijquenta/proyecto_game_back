#obtener datos con los parametros
#enviar data al generador de reportes
#devolver el reporte generado

from flask import make_response
from core.rml.report_generator import Report
from core.database import select

import pandas as pd

def make(pdf):
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format("archivo.pdf")
    response.mimetype = 'application/pdf'
    return response
    
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


def rptTotalesSigma():
    print("sql")
    params = select(f'''
        SELECT id, nombre_usuario, contrasena, nombre_completo, rol
        FROM usuarios;
    ''')
    print("params", params)
    return make(Report().RptTotalesSigma(params, 1))
    # return select(f'''
    #     SELECT da, ue, pg, proy, act, denominacion, total_indemnizacion FROM p_bsocial.bs_reporte_totales_sigma2(\'{fechaInicio}\', \'{fechaFin}\') AS 
    #     (da varchar, ue varchar, pg varchar, proy varchar, act varchar, denominacion varchar, total_indemnizacion numeric)
    # ''')
