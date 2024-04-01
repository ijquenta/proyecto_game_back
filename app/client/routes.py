apiVersion = "/academico_api"
auth = "/auth"
class Routes:
    index = apiVersion + '/'
    protected = apiVersion + '/secure'

    # Login y Register
    login = apiVersion + '/login'
    register = apiVersion + '/register'
    verify = apiVersion + '/verify/token'
    login2 = apiVersion + '/login2'
    register2 = apiVersion + '/register2'

    # Persona 
    gestionarPersona = apiVersion + '/gestionarPersona'
    eliminarPersona = apiVersion + '/eliminarPersona'
    tipoDocumento = apiVersion + '/tipoDocumento'
    tipoEstadoCivil = apiVersion + '/tipoEstadoCivil'
    tipoGenero = apiVersion + '/tipoGenero'
    tipoPais = apiVersion + '/tipoPais'
    tipoCiudad = apiVersion + '/tipoCiudad'
    registrarPersona = apiVersion + '/registrarPersona'
    listarPersona = apiVersion + '/listarPersona'

    # Usuario
    gestionarUsuario = apiVersion + '/gestionarUsuario'
    listaUsuario = apiVersion + '/listaUsuario'
    tipoPersona = apiVersion +'/tipoPersona'
    perfil = apiVersion + auth + '/perfil'
    listaUsuarios = apiVersion + '/listaUsuarios'

    # Roles
    listarRoles = apiVersion + '/listarRoles'
    crearRol = apiVersion + '/crearRol'
    modificarRol = apiVersion + '/modificarRol'
    eliminarRol = apiVersion + '/eliminarRol'
    
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
   
    # Rol
    gestionarRol = apiVersion + '/gestionarRol'
    
    # Estudiante
    listarEstudiante = apiVersion + '/listarEstudiante'
    obtenerMateriasInscritas = apiVersion + '/obtenerMateriasInscritas'
    
    # Docente
    listarDocente = apiVersion + '/listarDocente'
    obtenerMateriasAsignadas = apiVersion + '/obtenerMateriasAsignadas'

    # Nota
    listarNota = apiVersion + '/listarNota'
    gestionarNota = apiVersion + '/gestionarNota'
    listarNotaEstudiante = apiVersion + '/listarNotaEstudiante'
    listarNotaDocente = apiVersion + '/listarNotaDocente'
    listarNotaEstudianteMateria = apiVersion + '/listarNotaEstudianteMateria'
    listarNotaEstudianteCurso = apiVersion + '/listarNotaEstudianteCurso'
    rptNotaEstudianteMateria = apiVersion + '/rptNotaEstudianteMateria'
    
    # Pago
    listarPago = apiVersion + '/listarPago'
    listarPagoEstudiante = apiVersion + '/listarPagoEstudiante'
    listarPagoEstudianteMateria = apiVersion + '/listarPagoEstudianteMateria'
    listarPagoEstudiantesMateria = apiVersion + '/listarPagoEstudiantesMateria'
    listarPagoCurso = apiVersion + '/listarPagoCurso'
    gestionarPago = apiVersion + '/gestionarPago'
    tipoPago = apiVersion + '/tipoPago'
    getPayments = apiVersion + '/getPayments'
    insertarPago = apiVersion + '/insertarPago'
    modificarPago = apiVersion + '/modificarPago'
    asignarPagoInscripcion = apiVersion + '/asignarPagoInscripcion'
    obtenerUltimoPago = apiVersion + '/obtenerUltimoPago'
    
    # Asistencia
    listarAsistencia = apiVersion + '/listarAsistencia'
    
    # Material de Apoyo
    listarMaterial = apiVersion + '/listarMaterial'
    listarTexto = apiVersion + '/listarTexto'
    insertarTexto = apiVersion + '/insertarTexto'
    
    # Reportes
    rptTotalesSigma = apiVersion + '/rptTotalesSigma'