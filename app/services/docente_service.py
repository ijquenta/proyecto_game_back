from core.database import select, execute, execute_function, execute_response
from web.wsrrhh_service import *


def obtenerMateriasAsignadas(data):
    return select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.matid, m2.matnombre, cm.periddocente, p.pernomcompleto,
        cm.curmatfecini, 
        cm.curmatfecfin, cm.curmatestado, cm.curmatusureg, cm.curmatfecreg, cm.curmatusumod, cm.curmatfecmod, 
        cm.curmatestadodescripcion, cm.curmatidrol, cm.curmatidroldes, cm.curmatdescripcion 
        FROM academico.curso_materia cm
        inner join academico.persona p on p.perid = cm.periddocente
        left join academico.materia m2 on m2.matid = cm.matid 
        left join academico.curso c on c.curid = cm.curid 
        where cm.periddocente = {data['perid']}
    ''')
    
def listarDocente():
    return select('''
        SELECT p.perid, p.pernomcompleto, p.pernombres, p.perapepat, p.perapemat, 
        p.pertipodoc, td.tipodocnombre, 
        p.pernrodoc, p.perfecnac, p.perdirec, p.peremail, p.percelular, p.pertelefono, 
        p.perpais, tp.paisnombre, 
        p.perciudad, tc.ciudadnombre,
        p.pergenero, tg.generonombre,
        p.perestcivil, te.estadocivilnombre,
        p.perfoto, p.perestado, p.perobservacion, p.perusureg, p.perfecreg, p.perusumod, p.perfecmod,
        u.usuid, u.usuname, u.usuemail, u.usuimagen  
        FROM academico.persona p
        left join academico.usuario u on u.perid = p.perid
        left join academico.rol r on r.rolid = u.rolid
        left join academico.tipo_documento td on td.tipodocid = p.pertipodoc
        left join academico.tipo_pais tp on tp.paisid = p.perpais
        left join academico.tipo_ciudad tc on tc.ciudadid = p.perciudad
        left join academico.tipo_genero tg on tg.generoid = p.pergenero
        left join academico.tipo_estadocivil te on te.estadocivilid = p.perestcivil    
        where r.rolnombre = 'Docente'
        order by p.pernomcompleto
    ''')


def registrarPersona(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT * FROM academico.registrar_persona
                ({pernombres}, {perapepat}, {perapemat}, 
                 {pertipodoc}, {pernrodoc},  {perusureg} 
                )
        ''').format(
            pernombres=sql.Literal(data['pernombres']),
            perapepat=sql.Literal(data['perapepat']),
            perapemat=sql.Literal(data['perapemat']),
            pertipodoc=sql.Literal(data['pertipodoc']),
            pernrodoc=sql.Literal(data['pernrodoc']),
            perusureg=sql.Literal(data['perusureg'])
        )
        result = execute_response(as_string(query)) 
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def gestionarPersona(data):
    result = {'code': 0, 'message': 'No hay datos disponibles'}, 404
    try:
        query = sql.SQL('''
            SELECT academico.f_gestionar_persona
                ({tipo},{perid}, {pernombres}, {perapepat}, {perapemat}, 
                 {pertipodoc}, {pernrodoc}, {perfecnac}, {perdirec}, {peremail}, 
                 {percelular}, {pertelefono}, {perpais}, {perciudad}, {pergenero}, 
                 {perestcivil}, {perfoto}, {perestado}, {perobservacion}, {perusureg}, 
                 {perusumod})
        ''').format(
            tipo=sql.Literal(data['tipo']),
            perid=sql.Literal(data['perid']),
            pernombres=sql.Literal(data['pernombres']),
            perapepat=sql.Literal(data['perapepat']),
            perapemat=sql.Literal(data['perapemat']),
            pertipodoc=sql.Literal(data['pertipodoc']),
            pernrodoc=sql.Literal(data['pernrodoc']),
            perfecnac=sql.Literal(data['perfecnac']),
            perdirec=sql.Literal(data['perdirec']),
            peremail=sql.Literal(data['peremail']),
            percelular=sql.Literal(data['percelular']),
            pertelefono=sql.Literal(data['pertelefono']),
            perpais=sql.Literal(data['perpais']),
            perciudad=sql.Literal(data['perciudad']),
            pergenero=sql.Literal(data['pergenero']),
            perestcivil=sql.Literal(data['perestcivil']),
            perfoto=sql.Literal(data['perfoto']),
            perestado=sql.Literal(data['perestado']),
            perobservacion=sql.Literal(data['perobservacion']),
            perusureg=sql.Literal(data['perusureg']),
            perusumod=sql.Literal(data['perusumod']),
        )
        result = execute(as_string(query)) 
    except Exception as err:
        print(err)
        return {'code': 0, 'message': 'Error: ' + str(err)}, 404
    return result

def tipoDocumento():
    return select('''
        SELECT tipodocid, tipodocnombre
        FROM academico.tipo_documento;
    ''')
def tipoEstadoCivil():
    return select('''
        SELECT estadocivilid, estadocivilnombre
        FROM academico.tipo_estadocivil;
    ''')
def tipoGenero():
    return select('''
        SELECT generoid, generonombre
        FROM academico.tipo_genero;
    ''')
def tipoPais():
    return select('''
        SELECT paisid, paisnombre
        FROM academico.tipo_pais;
    ''')
def tipoCiudad():
    return select('''
        SELECT ciudadid, ciudadnombre, paisid
        FROM academico.tipo_ciudad;
    ''')
    
def listarUsuarios():
    return select(f'''
    SELECT id, nombre_usuario, contrasena, nombre_completo, rol
    FROM public.usuarios;
    ''')

def obtenerDatosDocente(nroCi, nomCompleto):
    return getDatosDocente(nroCi, nomCompleto)

def listarBeneficiosDocenteGrilla2(data):
    return select(f''' 
                SELECT b.nro_liquidacion,
                (select distinct substr(cod_ape_pro,1,2)||'-'||(case when facultad is null then '' else facultad end)
                from p_bsocial.t_beneficios_designaciones_meses  where  cod_docente=b.cod_docente and nro_liquidacion= b.nro_liquidacion)  as apepro_fac,
                  b.cod_docente,b.nombre_completo,b.nro_ci,b.ano,b.mes,b.nro_dictamen, b.hoja_ruta, b.fec_liquidacion, b.fec_ingrec,
                  b.fec_conclusion,b.fec_retiro,b.observaciones, b.ts_ano,
                        b.ts_mes, b.ts_dia, m.cod_tipo_motivo||'-'||m.des_tipo_motivo as motivo,b.fec_mod,b.usu_mod,sum(b.monto_tindemnizacion) as total_tindemnizacion
                   FROM  p_bsocial.t_beneficios b
                   JOIN p_bsocial.t_tipos_motivos m USING(cod_tipo_motivo)
                   WHERE b.cod_docente=\'{data['cod_docente']}\'
                   and b.estado_pla=1
                   AND b.ano={data['ano']}
                   AND b.mes={data['mes']}
                   GROUP BY b.cod_docente, b.nombre_completo,b.nro_ci, b.ano,b.mes,b.nro_dictamen, b.hoja_ruta,
                   b.fec_liquidacion, b.fec_ingrec,b.fec_conclusion, b.fec_retiro,b.observaciones, b.ts_ano,
                          b.ts_mes, b.ts_dia, motivo,b.fec_mod,b.usu_mod,b.nro_liquidacion,apepro_fac
    ''')

def listarTipoMotivo():
    return select(f'''select cod_tipo_motivo, des_tipo_motivo  from bd_bsocialdocente.p_bsocial.t_tipos_motivos order by cod_tipo_motivo ''')

def listarTresUltimosMesesRemuneraadosDocente(cod_docente, ano, mes):
    return listarTresUltimosMeses(cod_docente, ano, mes)   

def registrarTresMesesDoc(data):
    return getTresUltimosMesesDoc(data['cod_docente'], data['ano'], data['mes'])


def obtenerDatosModificar(data):
    return select(f''' 
    SELECT b.cod_docente, b.nro_liquidacion, b.nro_dictamen, b.hoja_ruta, b.fec_liquidacion, b.fec_ingrec, b.fec_conclusion,b.fec_retiro,b.observaciones, b.ts_ano,
      b.ts_mes, b.ts_dia, SUM(i.sp_ano) as sp_ano, SUM(i.sp_mes) as sp_mes, SUM(i.sp_dia) as sp_dia, m.cod_tipo_motivo||'-'||m.des_tipo_motivo as motivo
    FROM p_bsocial.t_beneficios_designaciones i JOIN p_bsocial.t_beneficios b USING(ano, mes, cod_docente)
    JOIN p_bsocial.t_tipos_motivos m USING(cod_tipo_motivo)
    WHERE b.cod_docente= \'{data['cod_docente']}\' AND b.ano={data['ano']} AND b.mes={data['mes']}
    GROUP BY b.cod_docente, b.nro_liquidacion, b.nro_dictamen, b.hoja_ruta, b.fec_liquidacion, b.fec_ingrec,b.fec_conclusion, b.fec_retiro,b.observaciones, b.ts_ano,
      b.ts_mes, b.ts_dia, motivo
    ''')

def registrarBeneficioNuevo(data):
    return select(f'''
    select * from p_bsocial.bs08_aplicar_beneficios_docente_form2({data['ano']}, {data['mes']},\'{data['codDocente']}\', {data['codTipoMotivo']}, \'{data['nroDictamen']}\', \'{data['hojaRuta']}\', \'{data['fecLiquidacion']}\', \'{data['fecIngrec']}\', \'{data['fecConclusion']}\', \'{data['fecRetiro']}\', {data['tsAno']}, {data['tsMes']}, {data['tsDia']}, \'{data['observaciones']}\', \'{data['usuarioReg']}\')
    ''')

def eliminarBeneficio(data):
    return select(f'''
    select * from p_bsocial.bs06_eliminar_liquidacion_docente({data['ano']}, {data['mes']}, \'{data['codDocente']} \', \'{data['observacion']} \' , \'{data['usuarioReg']} \' )
    ''')