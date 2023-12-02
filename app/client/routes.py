apiVersion = "/academico_api"
auth = "/auth"
class Routes:
    index = apiVersion + '/'
    protected = apiVersion + '/secure'

    # Persona 
    gestionarPersona = apiVersion + '/gestionarPersona'
    tipoDocumento = apiVersion + '/tipoDocumento'
    tipoEstadoCivil = apiVersion + '/tipoEstadoCivil'
    tipoGenero = apiVersion + '/tipoGenero'
    tipoPais = apiVersion + '/tipoPais'
    tipoCiudad = apiVersion + '/tipoCiudad'
    registrarPersona = apiVersion + '/registrarPersona'

    # Usuario
    gestionarUsuario = apiVersion + '/gestionarUsuario'
    listaUsuario = apiVersion + '/listaUsuario'
    tipoPersona = apiVersion +'/tipoPersona'
    perfil = apiVersion + auth + '/perfil'

    rptTotalesSigma = apiVersion + '/rptTotalesSigma'

    listaUsuarios = apiVersion + '/listaUsuarios'


    listarRoles = apiVersion + '/listarRoles'
    crearRol = apiVersion + '/crearRol'
    modificarRol = apiVersion + '/modificarRol'
    eliminarRol = apiVersion + '/eliminarRol'
    
    
    listarPersona = apiVersion + '/listarPersona'
    
    # Materia
    listarMateria = apiVersion + '/listarMateria'
    eliminarMateria = apiVersion + '/eliminarMateria'
    insertarMateria = apiVersion + '/insertarMateria'
    modificarMateria = apiVersion + '/modificarMateria'
    
    
    #Curso - Materia
    listarCursoMateria = apiVersion + '/listarCursoMateria'
    eliminarCursoMateria = apiVersion + '/eliminarCursoMateria'
    insertarCursoMateria = apiVersion + '/insertarCursoMateria'
    modificarCursoMateria = apiVersion + '/modificarCursoMateria'
    tipoRol = apiVersion + '/tipoRol'
    
    # Combo
    listaCursoCombo = apiVersion + '/listaCursoCombo'
    listaMateriaCombo = apiVersion + '/listaMateriaCombo'
    listaPersonaDocenteCombo = apiVersion + '/listaPersonaDocenteCombo'
    
    #Nivel
    listarNivel = apiVersion + '/listarNivel'
    insertarNivel = apiVersion + '/insertarNivel'
    modificarNivel = apiVersion + '/modificarNivel'
    eliminarNivel = apiVersion + '/eliminarNivel'
    
    #Incripcion
    listarInscripcion = apiVersion + '/listarInscripcion'
    insertarInscripcion = apiVersion + '/insertarInscripcion'
    modificarInscripcion = apiVersion + '/modificarInscripcion'
    eliminarInscripcion = apiVersion + '/eliminarInscripcion'
    obtenerCursoMateria = apiVersion + '/obtenerCursoMateria'
    listarComboCursoMateria = apiVersion + '/listarComboCursoMateria'
    listarComboMatricula = apiVersion + '/listarComboMatricula'


    #Matricula
    listarMatricula = apiVersion + '/listarMatricula'
    insertarMatricula = apiVersion + '/insertarMatricula'
    modificarMatricula = apiVersion + '/modificarMatricula'
    eliminarMatricula = apiVersion + '/eliminarMatricula'

    login = apiVersion + '/login'
    register = apiVersion + '/register'
    verify = apiVersion + '/verify/token'
    
    
    login2 = apiVersion + '/login2'
    register2 = apiVersion + '/register2'
    
    # Rol
    gestionarRol = apiVersion + '/gestionarRol'
    
    
    
    #Estudiante
    listarEstudiante = apiVersion + '/listarEstudiante'
    
    #Docente
    listarDocente = apiVersion + '/listarDocente'

    #Nota
    listarNota = apiVersion + '/listarNota'
    
    #Pago
    listarPago = apiVersion + '/listarPago'
    
    #Asistencia
    listarAsistencia = apiVersion + '/listarAsistencia'
    
    #Material
    listarMaterial = apiVersion + '/listarMaterial'