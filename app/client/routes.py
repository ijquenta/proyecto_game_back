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
    
    # Materia
    listarMaterias = apiVersion + '/listarMaterias'
    
    
    #Curso - Materia
    listarCursoMateria = apiVersion + '/listarCursoMateria'
    
    # Combo
    listaCursoCombo = apiVersion + '/listaCursoCombo'
    listaMateriaCombo = apiVersion + '/listaMateriaCombo'
    listaPersonaDocenteCombo = apiVersion + '/listaPersonaDocenteCombo'
    
    #Nivel
    listarNivel = apiVersion + '/listarNivel'
    insertarNivel = apiVersion + '/insertarNivel'
    
    

    login = apiVersion + '/login'
    register = apiVersion + 'register'
    verify = apiVersion + '/verify/token'


    