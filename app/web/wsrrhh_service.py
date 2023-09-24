import requests
from core.configuration import WS_API_URL, API_SECRET_KEY
import json
from core.database import execute, as_string
from psycopg2 import sql
# Existe redundancia de codigo? si, pero funciona xD
headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json" ,
    "x-api-key": API_SECRET_KEY
    }

def catchError():
    def intermediate(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as err:
                return {'code':0, 'message':'No se encuentra habilitado el ws'}, 200
        return wrapper
    return intermediate

@catchError()
def getDatosDocente(nroCi, nomCompleto):
    reqUrl = f"{WS_API_URL}/obtenerDatosPersonaDocente"

    payload = {
        "nroCi": str(nroCi),
        "nomCompleto": str(nomCompleto)
    }

    result = requests.request("POST", reqUrl, json=payload, headers = headersList)
    #print(result.json())
    return result.json()

def listarTresUltimosMeses(cod_docente, ano, mes):
    reqUrl = f"{WS_API_URL}/enlaceLic"

    payload = {
        "cod_docente": str(cod_docente),
        "ano": int(ano),
        "mes": int(mes)
    }

    result = requests.request("POST", reqUrl, json=payload, headers = headersList)
    return result.json()
    
@catchError()
def getTresUltimosMesesDoc(cod_docente, ano, mes):
    reqUrl = f"{WS_API_URL}/enlaceLic"

    payload = {
        "cod_docente": str(cod_docente),
        "ano": int(ano),
        "mes": int(mes)
    }
    response = requests.request("POST", reqUrl, json=payload, headers = headersList)
    return insertarTresUltimosMeses(response.json())
@catchError()
def insertarTresUltimosMeses(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    # print(data)
    # print("---")
    # print(data[0])
    cont = 1
    for i in data:
        try:
            query = sql.SQL(
                '''
                INSERT INTO p_bsocial.t_beneficios_temporal 
                (
                    cod_docente, uni_ejecutora, ano, mes, tg_ano, tg_mes
                )
                VALUES 
                ({codDocente}, {iniEjecutora}, {idGestion}, {idMes}, {idGestionTg}, {idMesTg})
                '''
                ).format(codDocente=sql.Literal(i['cod_docente']),
                    iniEjecutora=sql.Literal(i['uni_ejecutora']),
                    idGestion=sql.Literal(i['ano']),
                    idMes=sql.Literal(i['mes']),
                    idGestionTg=sql.Literal(i['tg_ano']),
                    idMesTg=sql.Literal(i['tg_mes'])
                )  
            # print(i['mes'])
            result = execute(as_string(query))
        
        except Exception as err:
            print(err)
            return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    # print(cont)
    # cont = cont + 1
    return result

"""

@catchError()
def getMesesRestaurables(idGestion, idPersona):
    reqUrl = f"{WS_API_URL}/obtenerPlanillaAdmConsolidaMeses"

    payload = {
        "idGestion": int(idGestion),
        "idPersona": int(idPersona)
    }

    response = requests.request("POST", reqUrl, json=payload, headers = headersList)

    if response.status_code != 200:
        return response.json(), 404

    return response.json()

"""


"""

@catchError()
def getPlanillaAdministrativaPersona(idGestion, idMes, idPersona, idUsuario):
    reqUrl = f"{WS_API_URL}/obtenerPlanillaAdmConsolida"

    payload = {
        "idGestion": int(idGestion),
        "idMes": int(idMes),
        "idPersona": int(idPersona)
    }

    response = requests.request("PUT", reqUrl, json=payload, headers = headersList)

    if response.status_code != 200:
        return response.json(), 404

    result = execute(f'''update public.planilla_regular 
	    set estado = 0,
		fec_modificacion = current_timestamp,  
		id_usuario_modificacion = {idUsuario}
	    where id_mes = {idMes} and id_gestion = {idGestion} and estado = 1 and id_persona = {idPersona}''')

    if result[0]['code'] == 1:
        return insertarPlanilla(response.json(), idUsuario)
    return result

@catchError()
def insertarPlanilla(data, idUsuario):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    for i in data:
        try:
            query = sql.SQL(
                '''
                INSERT INTO public.planilla_regular
                (
                    id_rha_pmensual_mhaberes,id_gestion,id_mes,des_mes,id_persona,paterno,materno,casada,nombres,nombre_completo,ci,ci_sc,ci_expedido,id_rha_pm_designacion,id_rha_tipo_designacion,tipo_designacion_descripcion,fecha_inicio_mensual,fecha_final_mensual,fecha_inicio_memorandum,fecha_final_memorandum,id_tipo_ingreso,tipo_ingreso_descripcion,id_rha_tipo_autoridad,tipo_autoridad_descripcion,id_rha_presupuesto_item,id_sexo,sexo,fecha_nacimiento,id_gestion_ingreso,id_mes_ingreso,id_rha_autoridad,autoridad_descripcion,id_rha_cargo_presupuesto,cargo_presupuesto,id_rha_nivel_presupuesto,nivel_presupuesto,id_rha_partida_presupuesto,partida_presupuesto,id_rha_tiempo_presupuesto,tiempo_presupuesto,id_cargo_ejecutado,cargo_ejecutado,cargo_ejecutado_2,id_nivel_ejecutado,nivel_ejecutado_descripcion,id_rha_partida_ejecutado,partida_ejecutado,id_rha_tiempo_ejecutado,tiempo_ejecutado,id_apertura,apertura_descripcion,apertura_abreviado,id_apertura_padre,apertura_descripcion_padre,apertura_abreviado_padre,codigo_apertura,uni_ejecutora,nro_programa,nro_subprograma,nro_proyecto,nro_actividad,nro_tarea,nro_subtarea,nro_otro,item,dias_trabajados,fecha_antiguedad,puntaje_salarial,monto_salarial,id_grado_academico,estudio,puntaje_profesional,monto_profesional,puntaje_evaluacion,monto_evaluacion,monto_thbasico,monto_thbasico_real,porcentaje_antiguedad,monto_antiguedad,monto_antiguedad_real,monto_tganado,monto_tganado_real,monto_taporte,monto_tdescuento,monto_tliquido,monto_tliquido_real,estado,id_usuario_registro,fec_registro,id_usuario_modificacion,fec_modificacion,da,ue,pg,proy,act,apertura_2,cuenta_bancaria,numero_cheque,numero_boleta,adm_doc,otro_sueldo,otro_sueldo_in,nua_afp,anios_antiguedad,id_entidad,id_tipo_aportante,cod_aporte,aporte_porcentaje,aporte_monto,aporte_monto_2,edad,ap_solidario_porcentaje,ap_solidario_monto,ap_nacional_porcentaje,ap_nacional_monto,ap_renta_porcentaje,ap_renta_monto,ap_riesgo_porcentaje,ap_riesgo_monto,ap_comision_porcentaje,ap_comision_monto,ap_nacional_diferencia,tipo_aportante,tipo_aportante_abreviacion,entidad,entidad_abreviacion,app1_porcentaje,app1_monto,app2_porcentaje,app2_monto,app3_porcentaje,app3_monto,app4_porcentaje,app4_monto,app5_porcentaje,app5_monto,app6_porcentaje,app6_monto,app7_porcentaje,app7_monto,app8_porcentaje,app8_monto,sueldo_neto,minimo_salarios,cantidad_minsal,diferencia,imp_porc,monto_facturas,porcentaje_facturas,porc_sal_min,saldo_fisco,sal_depen,saldo_iva_acumulado,porc_inc_ufv,saldo_actualizado,saldo_t_dep,saldo_utilizado,imp_ret,saldo_mes_siguiente,renta_monto_reintegro,id_rha_pm_mimpositiva,descuento1_des,descuento1_des_abrev,descuento1_monto,descuento2_des,descuento2_des_abrev,descuento2_monto,descuento3_des,descuento3_des_abrev,descuento3_monto,descuento4_des,descuento4_des_abrev,descuento4_monto,descuento5_des,descuento5_des_abrev,descuento5_monto,descuento6_des,descuento6_des_abrev,descuento6_monto,descuento7_des,descuento7_des_abrev,descuento7_monto,descuento8_des,descuento8_des_abrev,descuento8_monto,descuento9_des,descuento9_des_abrev,descuento9_monto,descuento10_des,descuento10_des_abrev,descuento10_monto,descuento11_des,descuento11_des_abrev,descuento11_monto,descuento12_des,descuento12_des_abrev,descuento12_monto,descuento13_des,descuento13_des_abrev,descuento13_monto,descuento14_des,descuento14_des_abrev,descuento14_monto,descuento15_des,descuento15_des_abrev,descuento15_monto,descuento16_des,descuento16_des_abrev,descuento16_monto,descuento17_des,descuento17_des_abrev,descuento17_monto,descuento18_des,descuento18_des_abrev,descuento18_monto,descuento19_des,descuento19_des_abrev,descuento19_monto,descuento20_des,descuento20_des_abrev,descuento20_monto,descuento21_des,descuento21_des_abrev,descuento21_monto,descuento22_des,descuento22_des_abrev,descuento22_monto,descuento23_des,descuento23_des_abrev,descuento23_monto,descuento24_des,descuento24_des_abrev,descuento24_monto,descuento25_des,descuento25_des_abrev,descuento25_monto,descuento26_des,descuento26_des_abrev,descuento26_monto,descuento27_des,descuento27_des_abrev,descuento27_monto,descuento28_des,descuento28_des_abrev,descuento28_monto,descuento29_des,descuento29_des_abrev,descuento29_monto,descuento30_des,descuento30_des_abrev,descuento30_monto,saldo_rg_acumulado,monto_extra,monto_suplencia,id_tipo_licencia,desc_tipo_licencia,monto_sueldo_docente,monto_sueldo_administrativo,con_descuentos,orden_aportante,fec_recuperado,estado_recuperado,id_entidad_bancaria,id_tipo_titulo,desc_tipo_titulo,id_persona_consolida,url_boleta,tipo_ci,direccion,correo,celular,otro_sueldo_1,otro_sueldo_2,tipo_modificacion,id_gestion_procesado,id_mes_procesado,correlativo_liquidacion,gestion_liquidacion
                )
                VALUES
                ({idRhaPmensualMhaberes},{idGestion},{idMes},{desMes},{idPersona},{paterno},{materno},{casada},{nombres},{nombreCompleto},{ci},{ciSc},{ciExpedido},{idRhaPmDesignacion},{idRhaTipoDesignacion},{tipoDesignacionDescripcion},{fechaInicioMensual},{fechaFinalMensual},{fechaInicioMemorandum},{fechaFinalMemorandum},{idTipoIngreso},{tipoIngresoDescripcion},{idRhaTipoAutoridad},{tipoAutoridadDescripcion},{idRhaPresupuestoItem},{idSexo},{sexo},{fechaNacimiento},{idGestionIngreso},{idMesIngreso},{idRhaAutoridad},{autoridadDescripcion},{idRhaCargoPresupuesto},{cargoPresupuesto},{idRhaNivelPresupuesto},{nivelPresupuesto},{idRhaPartidaPresupuesto},{partidaPresupuesto},{idRhaTiempoPresupuesto},{tiempoPresupuesto},{idCargoEjecutado},{cargoEjecutado},{cargoEjecutado2},{idNivelEjecutado},{nivelEjecutadoDescripcion},{idRhaPartidaEjecutado},{partidaEjecutado},{idRhaTiempoEjecutado},{tiempoEjecutado},{idApertura},{aperturaDescripcion},{aperturaAbreviado},{idAperturaPadre},{aperturaDescripcionPadre},{aperturaAbreviadoPadre},{codigoApertura},{uniEjecutora},{nroPrograma},{nroSubprograma},{nroProyecto},{nroActividad},{nroTarea},{nroSubtarea},{nroOtro},{item},{diasTrabajados},{fechaAntiguedad},{puntajeSalarial},{montoSalarial},{idGradoAcademico},{estudio},{puntajeProfesional},{montoProfesional},{puntajeEvaluacion},{montoEvaluacion},{montoThbasico},{montoThbasicoReal},{porcentajeAntiguedad},{montoAntiguedad},{montoAntiguedadReal},{montoTganado},{montoTganadoReal},{montoTaporte},{montoTdescuento},{montoTliquido},{montoTliquidoReal},{estado},{idUsuarioRegistro},current_timestamp,{idUsuarioModificacion},{fecModificacion},{da},{ue},{pg},{proy},{act},{apertura2},{cuentaBancaria},{numeroCheque},{numeroBoleta},{admDoc},{otroSueldo},{otroSueldoIn},{nuaAfp},{aniosAntiguedad},{idEntidad},{idTipoAportante},{codAporte},{aportePorcentaje},{aporteMonto},{aporteMonto2},{edad},{apSolidarioPorcentaje},{apSolidarioMonto},{apNacionalPorcentaje},{apNacionalMonto},{apRentaPorcentaje},{apRentaMonto},{apRiesgoPorcentaje},{apRiesgoMonto},{apComisionPorcentaje},{apComisionMonto},{apNacionalDiferencia},{tipoAportante},{tipoAportanteAbreviacion},{entidad},{entidadAbreviacion},{app1Porcentaje},{app1Monto},{app2Porcentaje},{app2Monto},{app3Porcentaje},{app3Monto},{app4Porcentaje},{app4Monto},{app5Porcentaje},{app5Monto},{app6Porcentaje},{app6Monto},{app7Porcentaje},{app7Monto},{app8Porcentaje},{app8Monto},{sueldoNeto},{minimoSalarios},{cantidadMinsal},{diferencia},{impPorc},{montoFacturas},{porcentajeFacturas},{porcSalMin},{saldoFisco},{salDepen},{saldoIvaAcumulado},{porcIncUfv},{saldoActualizado},{saldoTDep},{saldoUtilizado},{impRet},{saldoMesSiguiente},{rentaMontoReintegro},{idRhaPmMimpositiva},{descuento1Des},{descuento1DesAbrev},{descuento1Monto},{descuento2Des},{descuento2DesAbrev},{descuento2Monto},{descuento3Des},{descuento3DesAbrev},{descuento3Monto},{descuento4Des},{descuento4DesAbrev},{descuento4Monto},{descuento5Des},{descuento5DesAbrev},{descuento5Monto},{descuento6Des},{descuento6DesAbrev},{descuento6Monto},{descuento7Des},{descuento7DesAbrev},{descuento7Monto},{descuento8Des},{descuento8DesAbrev},{descuento8Monto},{descuento9Des},{descuento9DesAbrev},{descuento9Monto},{descuento10Des},{descuento10DesAbrev},{descuento10Monto},{descuento11Des},{descuento11DesAbrev},{descuento11Monto},{descuento12Des},{descuento12DesAbrev},{descuento12Monto},{descuento13Des},{descuento13DesAbrev},{descuento13Monto},{descuento14Des},{descuento14DesAbrev},{descuento14Monto},{descuento15Des},{descuento15DesAbrev},{descuento15Monto},{descuento16Des},{descuento16DesAbrev},{descuento16Monto},{descuento17Des},{descuento17DesAbrev},{descuento17Monto},{descuento18Des},{descuento18DesAbrev},{descuento18Monto},{descuento19Des},{descuento19DesAbrev},{descuento19Monto},{descuento20Des},{descuento20DesAbrev},{descuento20Monto},{descuento21Des},{descuento21DesAbrev},{descuento21Monto},{descuento22Des},{descuento22DesAbrev},{descuento22Monto},{descuento23Des},{descuento23DesAbrev},{descuento23Monto},{descuento24Des},{descuento24DesAbrev},{descuento24Monto},{descuento25Des},{descuento25DesAbrev},{descuento25Monto},{descuento26Des},{descuento26DesAbrev},{descuento26Monto},{descuento27Des},{descuento27DesAbrev},{descuento27Monto},{descuento28Des},{descuento28DesAbrev},{descuento28Monto},{descuento29Des},{descuento29DesAbrev},{descuento29Monto},{descuento30Des},{descuento30DesAbrev},{descuento30Monto},{saldoRgAcumulado},{montoExtra},{montoSuplencia},{idTipoLicencia},{descTipoLicencia},{montoSueldoDocente},{montoSueldoAdministrativo},{conDescuentos},{ordenAportante},{fecRecuperado},{estadoRecuperado},{idEntidadBancaria},{idTipoTitulo},{descTipoTitulo},{idPersonaConsolida},{urlBoleta},{tipoCi},{direccion},{correo},{celular},{otroSueldo1},{otroSueldo2},{tipoModificacion},{idGestionProcesado},{idMesProcesado},{correlativoLiquidacion},{gestionLiquidacion})
                ''').format(
                    idRhaPmensualMhaberes = sql.Literal(i['idRhaPmensualMhaberes']), idGestion = sql.Literal(i['idGestion']), idMes = sql.Literal(i['idMes']), desMes = sql.Literal(i['desMes']), idPersona = sql.Literal(i['idPersona']), paterno = sql.Literal(i['paterno']), materno = sql.Literal(i['materno']), 
                    casada = sql.Literal(i['casada']), nombres = sql.Literal(i['nombres']), nombreCompleto = sql.Literal(i['nombreCompleto']), ci = sql.Literal(i['ci']), ciSc = sql.Literal(i['ciSc']), ciExpedido = sql.Literal(i['ciExpedido']), idRhaPmDesignacion = sql.Literal(i['idRhaPmDesignacion']), idRhaTipoDesignacion = sql.Literal(i['idRhaTipoDesignacion']), tipoDesignacionDescripcion = sql.Literal(i['tipoDesignacionDescripcion']), fechaInicioMensual = sql.Literal(i['fechaInicioMensual']), fechaFinalMensual = sql.Literal(i['fechaFinalMensual']), fechaInicioMemorandum = sql.Literal(i['fechaInicioMemorandum']), fechaFinalMemorandum = sql.Literal(i['fechaFinalMemorandum']), idTipoIngreso = sql.Literal(i['idTipoIngreso']), tipoIngresoDescripcion = sql.Literal(i['tipoIngresoDescripcion']), idRhaTipoAutoridad = sql.Literal(i['idRhaTipoAutoridad']), tipoAutoridadDescripcion = sql.Literal(i['tipoAutoridadDescripcion']), idRhaPresupuestoItem = sql.Literal(i['idRhaPresupuestoItem']), idSexo = sql.Literal(i['idSexo']), sexo = sql.Literal(i['sexo']), fechaNacimiento = sql.Literal(i['fechaNacimiento']), idGestionIngreso = sql.Literal(i['idGestionIngreso']), idMesIngreso = sql.Literal(i['idMesIngreso']), idRhaAutoridad = sql.Literal(i['idRhaAutoridad']), autoridadDescripcion = sql.Literal(i['autoridadDescripcion']), idRhaCargoPresupuesto = sql.Literal(i['idRhaCargoPresupuesto']), cargoPresupuesto = sql.Literal(i['cargoPresupuesto']), idRhaNivelPresupuesto = sql.Literal(i['idRhaNivelPresupuesto']), nivelPresupuesto = sql.Literal(i['nivelPresupuesto']), idRhaPartidaPresupuesto = sql.Literal(i['idRhaPartidaPresupuesto']), partidaPresupuesto = sql.Literal(i['partidaPresupuesto']), idRhaTiempoPresupuesto = sql.Literal(i['idRhaTiempoPresupuesto']), tiempoPresupuesto = sql.Literal(i['tiempoPresupuesto']), idCargoEjecutado = sql.Literal(i['idCargoEjecutado']), cargoEjecutado = sql.Literal(i['cargoEjecutado']), cargoEjecutado2 = sql.Literal(i['cargoEjecutado2']), idNivelEjecutado = sql.Literal(i['idNivelEjecutado']), nivelEjecutadoDescripcion = sql.Literal(i['nivelEjecutadoDescripcion']), idRhaPartidaEjecutado = sql.Literal(i['idRhaPartidaEjecutado']), partidaEjecutado = sql.Literal(i['partidaEjecutado']), idRhaTiempoEjecutado = sql.Literal(i['idRhaTiempoEjecutado']), tiempoEjecutado = sql.Literal(i['tiempoEjecutado']), idApertura = sql.Literal(i['idApertura']), aperturaDescripcion = sql.Literal(i['aperturaDescripcion']), aperturaAbreviado = sql.Literal(i['aperturaAbreviado']), idAperturaPadre = sql.Literal(i['idAperturaPadre']), aperturaDescripcionPadre = sql.Literal(i['aperturaDescripcionPadre']), aperturaAbreviadoPadre = sql.Literal(i['aperturaAbreviadoPadre']), codigoApertura = sql.Literal(i['codigoApertura']), uniEjecutora = sql.Literal(i['uniEjecutora']), nroPrograma = sql.Literal(i['nroPrograma']), nroSubprograma = sql.Literal(i['nroSubprograma']), nroProyecto = sql.Literal(i['nroProyecto']), nroActividad = sql.Literal(i['nroActividad']), nroTarea = sql.Literal(i['nroTarea']), nroSubtarea = sql.Literal(i['nroSubtarea']), nroOtro = sql.Literal(i['nroOtro']), item = sql.Literal(i['item']), diasTrabajados = sql.Literal(i['diasTrabajados']), fechaAntiguedad = sql.Literal(i['fechaAntiguedad']), puntajeSalarial = sql.Literal(i['puntajeSalarial']), montoSalarial = sql.Literal(i['montoSalarial']), idGradoAcademico = sql.Literal(i['idGradoAcademico']), estudio = sql.Literal(i['estudio']), puntajeProfesional = sql.Literal(i['puntajeProfesional']), montoProfesional = sql.Literal(i['montoProfesional']), puntajeEvaluacion = sql.Literal(i['puntajeEvaluacion']), montoEvaluacion = sql.Literal(i['montoEvaluacion']), montoThbasico = sql.Literal(i['montoThbasico']), montoThbasicoReal = sql.Literal(i['montoThbasicoReal']), porcentajeAntiguedad = sql.Literal(i['porcentajeAntiguedad']), montoAntiguedad = sql.Literal(i['montoAntiguedad']), montoAntiguedadReal = sql.Literal(i['montoAntiguedadReal']), montoTganado = sql.Literal(i['montoTganado']), montoTganadoReal = sql.Literal(i['montoTganadoReal']), montoTaporte = sql.Literal(i['montoTaporte']), montoTdescuento = sql.Literal(i['montoTdescuento']), montoTliquido = sql.Literal(i['montoTliquido']), montoTliquidoReal = sql.Literal(i['montoTliquidoReal']), estado = sql.Literal(i['estado']), idUsuarioRegistro = sql.Literal(idUsuario), fecRegistro = sql.Literal(i['fecRegistro']), idUsuarioModificacion = sql.Literal(i['idUsuarioModificacion']), fecModificacion = sql.Literal(i['fecModificacion']), da = sql.Literal(i['da']), ue = sql.Literal(i['ue']), pg = sql.Literal(i['pg']), proy = sql.Literal(i['proy']), act = sql.Literal(i['act']), apertura2 = sql.Literal(i['apertura2']), cuentaBancaria = sql.Literal(i['cuentaBancaria']), numeroCheque = sql.Literal(i['numeroCheque']), numeroBoleta = sql.Literal(i['numeroBoleta']), admDoc = sql.Literal(i['admDoc']), otroSueldo = sql.Literal(i['otroSueldo']), otroSueldoIn = sql.Literal(i['otroSueldoIn']), nuaAfp = sql.Literal(i['nuaAfp']), aniosAntiguedad = sql.Literal(i['aniosAntiguedad']), idEntidad = sql.Literal(i['idEntidad']), idTipoAportante = sql.Literal(i['idTipoAportante']), codAporte = sql.Literal(i['codAporte']), aportePorcentaje = sql.Literal(i['aportePorcentaje']), aporteMonto = sql.Literal(i['aporteMonto']), aporteMonto2 = sql.Literal(i['aporteMonto2']), edad = sql.Literal(i['edad']), apSolidarioPorcentaje = sql.Literal(i['apSolidarioPorcentaje']), apSolidarioMonto = sql.Literal(i['apSolidarioMonto']), apNacionalPorcentaje = sql.Literal(i['apNacionalPorcentaje']), apNacionalMonto = sql.Literal(i['apNacionalMonto']), apRentaPorcentaje = sql.Literal(i['apRentaPorcentaje']), apRentaMonto = sql.Literal(i['apRentaMonto']), apRiesgoPorcentaje = sql.Literal(i['apRiesgoPorcentaje']), apRiesgoMonto = sql.Literal(i['apRiesgoMonto']), apComisionPorcentaje = sql.Literal(i['apComisionPorcentaje']), apComisionMonto = sql.Literal(i['apComisionMonto']), apNacionalDiferencia = sql.Literal(i['apNacionalDiferencia']), tipoAportante = sql.Literal(i['tipoAportante']), tipoAportanteAbreviacion = sql.Literal(i['tipoAportanteAbreviacion']), entidad = sql.Literal(i['entidad']), entidadAbreviacion = sql.Literal(i['entidadAbreviacion']), app1Porcentaje = sql.Literal(i['app1Porcentaje']), app1Monto = sql.Literal(i['app1Monto']), app2Porcentaje = sql.Literal(i['app2Porcentaje']), app2Monto = sql.Literal(i['app2Monto']), app3Porcentaje = sql.Literal(i['app3Porcentaje']), app3Monto = sql.Literal(i['app3Monto']), app4Porcentaje = sql.Literal(i['app4Porcentaje']), app4Monto = sql.Literal(i['app4Monto']), app5Porcentaje = sql.Literal(i['app5Porcentaje']), app5Monto = sql.Literal(i['app5Monto']), app6Porcentaje = sql.Literal(i['app6Porcentaje']), app6Monto = sql.Literal(i['app6Monto']), app7Porcentaje = sql.Literal(i['app7Porcentaje']), app7Monto = sql.Literal(i['app7Monto']), app8Porcentaje = sql.Literal(i['app8Porcentaje']), app8Monto = sql.Literal(i['app8Monto']), sueldoNeto = sql.Literal(i['sueldoNeto']), minimoSalarios = sql.Literal(i['minimoSalarios']), cantidadMinsal = sql.Literal(i['cantidadMinsal']), diferencia = sql.Literal(i['diferencia']), impPorc = sql.Literal(i['impPorc']), montoFacturas = sql.Literal(i['montoFacturas']), porcentajeFacturas = sql.Literal(i['porcentajeFacturas']), porcSalMin = sql.Literal(i['porcSalMin']), saldoFisco = sql.Literal(i['saldoFisco']), salDepen = sql.Literal(i['salDepen']), saldoIvaAcumulado = sql.Literal(i['saldoIvaAcumulado']), porcIncUfv = sql.Literal(i['porcIncUfv']), saldoActualizado = sql.Literal(i['saldoActualizado']), saldoTDep = sql.Literal(i['saldoTDep']), saldoUtilizado = sql.Literal(i['saldoUtilizado']), impRet = sql.Literal(i['impRet']), saldoMesSiguiente = sql.Literal(i['saldoMesSiguiente']), rentaMontoReintegro = sql.Literal(i['rentaMontoReintegro']), idRhaPmMimpositiva = sql.Literal(i['idRhaPmMimpositiva']), descuento1Des = sql.Literal(i['descuento1Des']), descuento1DesAbrev = sql.Literal(i['descuento1DesAbrev']), descuento1Monto = sql.Literal(i['descuento1Monto']), descuento2Des = sql.Literal(i['descuento2Des']), descuento2DesAbrev = sql.Literal(i['descuento2DesAbrev']), descuento2Monto = sql.Literal(i['descuento2Monto']), descuento3Des = sql.Literal(i['descuento3Des']), descuento3DesAbrev = sql.Literal(i['descuento3DesAbrev']), descuento3Monto = sql.Literal(i['descuento3Monto']), descuento4Des = sql.Literal(i['descuento4Des']), descuento4DesAbrev = sql.Literal(i['descuento4DesAbrev']), descuento4Monto = sql.Literal(i['descuento4Monto']), descuento5Des = sql.Literal(i['descuento5Des']), descuento5DesAbrev = sql.Literal(i['descuento5DesAbrev']), descuento5Monto = sql.Literal(i['descuento5Monto']), descuento6Des = sql.Literal(i['descuento6Des']), descuento6DesAbrev = sql.Literal(i['descuento6DesAbrev']), descuento6Monto = sql.Literal(i['descuento6Monto']), descuento7Des = sql.Literal(i['descuento7Des']), descuento7DesAbrev = sql.Literal(i['descuento7DesAbrev']), descuento7Monto = sql.Literal(i['descuento7Monto']), descuento8Des = sql.Literal(i['descuento8Des']), descuento8DesAbrev = sql.Literal(i['descuento8DesAbrev']), descuento8Monto = sql.Literal(i['descuento8Monto']), descuento9Des = sql.Literal(i['descuento9Des']), descuento9DesAbrev = sql.Literal(i['descuento9DesAbrev']), descuento9Monto = sql.Literal(i['descuento9Monto']), descuento10Des = sql.Literal(i['descuento10Des']), descuento10DesAbrev = sql.Literal(i['descuento10DesAbrev']), descuento10Monto = sql.Literal(i['descuento10Monto']), descuento11Des = sql.Literal(i['descuento11Des']), descuento11DesAbrev = sql.Literal(i['descuento11DesAbrev']), descuento11Monto = sql.Literal(i['descuento11Monto']), descuento12Des = sql.Literal(i['descuento12Des']), descuento12DesAbrev = sql.Literal(i['descuento12DesAbrev']), descuento12Monto = sql.Literal(i['descuento12Monto']), descuento13Des = sql.Literal(i['descuento13Des']), descuento13DesAbrev = sql.Literal(i['descuento13DesAbrev']), descuento13Monto = sql.Literal(i['descuento13Monto']), descuento14Des = sql.Literal(i['descuento14Des']), descuento14DesAbrev = sql.Literal(i['descuento14DesAbrev']), descuento14Monto = sql.Literal(i['descuento14Monto']), descuento15Des = sql.Literal(i['descuento15Des']), descuento15DesAbrev = sql.Literal(i['descuento15DesAbrev']), descuento15Monto = sql.Literal(i['descuento15Monto']), descuento16Des = sql.Literal(i['descuento16Des']), descuento16DesAbrev = sql.Literal(i['descuento16DesAbrev']), 
                    descuento16Monto = sql.Literal(i['descuento16Monto']), descuento17Des = sql.Literal(i['descuento17Des']), descuento17DesAbrev = sql.Literal(i['descuento17DesAbrev']), descuento17Monto = sql.Literal(i['descuento17Monto']), descuento18Des = sql.Literal(i['descuento18Des']), descuento18DesAbrev = sql.Literal(i['descuento18DesAbrev']), descuento18Monto = sql.Literal(i['descuento18Monto']), descuento19Des = sql.Literal(i['descuento19Des']), descuento19DesAbrev = sql.Literal(i['descuento19DesAbrev']), descuento19Monto = sql.Literal(i['descuento19Monto']), descuento20Des = sql.Literal(i['descuento20Des']), descuento20DesAbrev = sql.Literal(i['descuento20DesAbrev']), descuento20Monto = sql.Literal(i['descuento20Monto']), descuento21Des = sql.Literal(i['descuento21Des']), descuento21DesAbrev = sql.Literal(i['descuento21DesAbrev']), descuento21Monto = sql.Literal(i['descuento21Monto']), descuento22Des = sql.Literal(i['descuento22Des']), descuento22DesAbrev = sql.Literal(i['descuento22DesAbrev']), descuento22Monto = sql.Literal(i['descuento22Monto']), descuento23Des = sql.Literal(i['descuento23Des']), descuento23DesAbrev = sql.Literal(i['descuento23DesAbrev']), descuento23Monto = sql.Literal(i['descuento23Monto']), descuento24Des = sql.Literal(i['descuento24Des']), descuento24DesAbrev = sql.Literal(i['descuento24DesAbrev']), descuento24Monto = sql.Literal(i['descuento24Monto']), descuento25Des = sql.Literal(i['descuento25Des']), descuento25DesAbrev = sql.Literal(i['descuento25DesAbrev']), descuento25Monto = sql.Literal(i['descuento25Monto']), descuento26Des = sql.Literal(i['descuento26Des']), descuento26DesAbrev = sql.Literal(i['descuento26DesAbrev']), descuento26Monto = sql.Literal(i['descuento26Monto']), descuento27Des = sql.Literal(i['descuento27Des']), descuento27DesAbrev = sql.Literal(i['descuento27DesAbrev']), descuento27Monto = sql.Literal(i['descuento27Monto']), descuento28Des = sql.Literal(i['descuento28Des']), descuento28DesAbrev = sql.Literal(i['descuento28DesAbrev']), descuento28Monto = sql.Literal(i['descuento28Monto']), descuento29Des = sql.Literal(i['descuento29Des']), descuento29DesAbrev = sql.Literal(i['descuento29DesAbrev']), descuento29Monto = sql.Literal(i['descuento29Monto']), descuento30Des = sql.Literal(i['descuento30Des']), descuento30DesAbrev = sql.Literal(i['descuento30DesAbrev']), descuento30Monto = sql.Literal(i['descuento30Monto']), saldoRgAcumulado = sql.Literal(i['saldoRgAcumulado']), montoExtra = sql.Literal(i['montoExtra']), montoSuplencia = sql.Literal(i['montoSuplencia']), idTipoLicencia = sql.Literal(i['idTipoLicencia']), descTipoLicencia = sql.Literal(i['descTipoLicencia']), montoSueldoDocente = sql.Literal(i['montoSueldoDocente']), montoSueldoAdministrativo = sql.Literal(i['montoSueldoAdministrativo']), conDescuentos = sql.Literal(i['conDescuentos']), ordenAportante = sql.Literal(i['ordenAportante']), fecRecuperado = sql.Literal(i['fecRecuperado']), estadoRecuperado = sql.Literal(i['estadoRecuperado']), idEntidadBancaria = sql.Literal(i['idEntidadBancaria']), idTipoTitulo = sql.Literal(i['idTipoTitulo']), descTipoTitulo = sql.Literal(i['descTipoTitulo']), idPersonaConsolida = sql.Literal(i['idPersonaConsolida']), urlBoleta = sql.Literal(i['urlBoleta']), tipoCi = sql.Literal(i['tipoCi']), direccion = sql.Literal(i['direccion']), correo = sql.Literal(i['correo']), celular = sql.Literal(i['celular']), otroSueldo1 = sql.Literal(i['otroSueldo1']), otroSueldo2 = sql.Literal(i['otroSueldo2']), tipoModificacion = sql.Literal(None), idGestionProcesado = sql.Literal(0), idMesProcesado = sql.Literal(0), correlativoLiquidacion = sql.Literal(0), gestionLiquidacion = sql.Literal(0)
                )
            result = execute(as_string(query))
        except Exception as err:
            print(err)
            return {'code': 0, 'message': 'Error: '+ str(err)}, 404
    return result

"""