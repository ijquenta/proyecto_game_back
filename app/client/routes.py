# apiVersion = "/calculobs_api"
#apiVersion = "/bsocial_api"
apiVersion = "/academico_api"
class Routes:
    index = apiVersion + '/'
    protected = apiVersion + '/secure'

    rptTotalesSigma = apiVersion + '/rptTotalesSigma'

    listaUsuarios = apiVersion + '/listaUsuarios'


    listarRoles = apiVersion + '/listarRoles'
    crearRol = apiVersion + '/crearRol'
    modificarRol = apiVersion + '/modificarRol'
    eliminarRol = apiVersion + '/eliminarRol'
    
    
    listarPersona = apiVersion + '/listarPersona'
    
    listarMaterias = apiVersion + '/listarMaterias'


    login = apiVersion + '/login'
    register = apiVersion + 'register'
    verify = apiVersion + '/verify/token'


    