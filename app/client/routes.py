# apiVersion = "/calculobs_api"
#apiVersion = "/bsocial_api"
apiVersion = "/academico_api"
class Routes:
    index = apiVersion + '/'
    protected = apiVersion + '/secure'

    rptTotalesSigma = apiVersion + '/rptTotalesSigma'

    listaUsuarios = apiVersion + '/listaUsuarios'

    obtenerDatosDocente = apiVersion + '/obtenerDatosDocente' 

    listarBeneficiosDocente = apiVersion + '/listarBeneficiosDocente'

    listarTipoMotivo = apiVersion + '/listarTipoMotivo'

    obtenerDatosModificar = apiVersion + '/obtenerDatosModificar'


    listarTresUltimosMesesRemuneraadosDocente = apiVersion + '/listarTresUltimosMesesRemuneraadosDocente'

    regTresUltMesRemDoc = apiVersion + '/regTresUltMesRemDoc'

    registrarBeneficioNuevo = apiVersion + '/registrarBeneficioNuevo'

    eliminarBeneficio = apiVersion + '/eliminarBeneficio'


    listarRoles = apiVersion + '/listarRoles'
    crearRol = apiVersion + '/crearRol'
    modificarRol = apiVersion + '/modificarRol'
    eliminarRol = apiVersion + '/eliminarRol'


    login = apiVersion + '/login'
    verify = apiVersion + '/verify/token'


    # actualizarBeneficiosSociales = apiVersion + '/actualizarBeneficiosSociales'
    # Ejemplo Insertar Registro en base de datos
    # regRestaurarMes = apiVersion + '/regRestaurarMes'
    