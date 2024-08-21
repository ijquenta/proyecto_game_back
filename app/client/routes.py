apiVersion = "/academico_api"
auth = "/auth"
class Routes:
    index = apiVersion + '/'
    protected = apiVersion + '/secure'

    # Routes for login and Register
    login = apiVersion + '/login'
    register = apiVersion + '/register'
    verify = apiVersion + '/verify/token'
    login2 = apiVersion + '/login2'
    register2 = apiVersion + '/register2'

    # Persona 
    managePerson = apiVersion + '/managePerson'
    deletePerson = apiVersion + '/deletePerson'
    deletePersonForm = apiVersion + '/deletePersonForm'
    tipoDocumento = apiVersion + '/tipoDocumento'
    tipoEstadoCivil = apiVersion + '/tipoEstadoCivil'
    tipoGenero = apiVersion + '/tipoGenero'
    tipoPais = apiVersion + '/tipoPais'
    tipoCiudad = apiVersion + '/tipoCiudad'
    createPersonForm = apiVersion + '/createPersonForm'
    getPersons = apiVersion + '/getPersons'
    updateProfile = apiVersion + '/updateProfile'
    showPersonData = apiVersion + '/showPersonData/<int:perid>'

    # Usuario
    gestionarUsuario = apiVersion + '/gestionarUsuario'
    gestionarUsuarioEstado = apiVersion + '/gestionarUsuarioEstado'
    gestionarUsuarioPassword = apiVersion + '/gestionarUsuarioPassword'
    listaUsuario = apiVersion + '/listaUsuario'
    tipoPersona = apiVersion +'/tipoPersona'
    tipoPersonaDocente = apiVersion +'/tipoPersonaDocente'
    perfil = apiVersion + auth + '/perfil'
    listaUsuarios = apiVersion + '/listaUsuarios'
    getUsers = apiVersion + '/getUsers'
    obtenerEmail = apiVersion + '/obtenerEmail'
    requestChangePassword = apiVersion + '/requestChangePassword'
    requestPasswordReset = apiVersion + '/auth/request-password-reset'
    resetPassword = apiVersion + '/auth/resetPassword/<string:token>'
    buscarUsuario = apiVersion + '/buscarUsuario'
    changePassword = apiVersion + '/changePassword'

    # Roles
    getRoles = apiVersion + '/getRoles'
    crearRol = apiVersion + '/crearRol'
    modificarRol = apiVersion + '/modificarRol'
    eliminarRol = apiVersion + '/eliminarRol'
    
    # Materia
    listarMateria = apiVersion + '/listarMateria'
    eliminarMateria = apiVersion + '/eliminarMateria'
    insertarMateria = apiVersion + '/insertarMateria'
    modificarMateria = apiVersion + '/modificarMateria'
    gestionarMateriaEstado = apiVersion + '/gestionarMateriaEstado'
    getMateriaById = apiVersion + '/getMateriaById/<int:matid>'
    
    #Curso - Materia
    listarCursoMateria = apiVersion + '/listarCursoMateria'
    eliminarCursoMateria = apiVersion + '/eliminarCursoMateria'
    insertarCursoMateria = apiVersion + '/insertarCursoMateria'
    modificarCursoMateria = apiVersion + '/modificarCursoMateria'
    gestionarCursoMateriaEstado = apiVersion + '/gestionarCursoMateriaEstado'
    tipoRol = apiVersion + '/tipoRol'
    getCursoById = apiVersion + '/getCursoById/<int:curid>'
    getTipoCurso = apiVersion + '/getTipoCurso'
    getTipoMateriaByCursoId = apiVersion + '/getTipoMateriaByCursoId/<int:curid>'

    
    # Combo
    listaCursoCombo = apiVersion + '/listaCursoCombo'
    listaMateriaCombo = apiVersion + '/listaMateriaCombo'
    getListMateriaCombo = apiVersion + '/getListMateriaCombo'
    listaPersonaDocenteCombo = apiVersion + '/listaPersonaDocenteCombo'
    
    
    #Nivel
    listarNivel = apiVersion + '/listarNivel'
    insertarNivel = apiVersion + '/insertarNivel'
    modificarNivel = apiVersion + '/modificarNivel'
    eliminarNivel = apiVersion + '/eliminarNivel'
    gestionarNivelEstado = apiVersion + '/gestionarNivelEstado'
    
    #Incripcion
    listarInscripcion = apiVersion + '/listarInscripcion'
    insertarInscripcion = apiVersion + '/insertarInscripcion'
    modificarInscripcion = apiVersion + '/modificarInscripcion'
    eliminarInscripcion = apiVersion + '/eliminarInscripcion'
    obtenerCursoMateria = apiVersion + '/obtenerCursoMateria'
    listarComboCursoMateria = apiVersion + '/listarComboCursoMateria'
    listarComboMatricula = apiVersion + '/listarComboMatricula'
    listarComboMatriculaEstudiante = apiVersion + '/listarComboMatriculaEstudiante'
    gestionarInscripcionEstado = apiVersion + '/gestionarInscripcionEstado'
    obtenerEstudiantesInscritos = apiVersion + '/obtenerEstudiantesInscritos'
    getCursoMateriaByIds = apiVersion + '/getCursoMateriaByIds'


    #Matricula
    listarMatricula = apiVersion + '/listarMatricula'
    insertarMatricula = apiVersion + '/insertarMatricula'
    modificarMatricula = apiVersion + '/modificarMatricula'
    eliminarMatricula = apiVersion + '/eliminarMatricula'
    gestionarMatriculaEstado = apiVersion + '/gestionarMatriculaEstado' 
    listarTipoMatricula = apiVersion + '/listarTipoMatricula'
    insertarTipoMatricula = apiVersion + '/insertarTipoMatricula'
    modificarTipoMatricula = apiVersion + '/modificarTipoMatricula'
    gestionarTipoMatriculaEstado = apiVersion + '/gestionarTipoMatriculaEstado'
    listarTipoMatriculaCombo = apiVersion + '/listarTipoMatriculaCombo'
    listarTipoPersonaEstudiante = apiVersion + '/listarTipoPersonaEstudiante'
   
    # Rol
    getRoles = apiVersion + '/getRoles'
    manageRole = apiVersion + '/manageRole'
    manageRoleStatus = apiVersion + '/manageRoleStatus'
    deleteRole = apiVersion + '/deleteRole/<int:rolid>'
    
    # Estudiante
    listarEstudiante = apiVersion + '/listarEstudiante'
    obtenerMateriasInscritas = apiVersion + '/obtenerMateriasInscritas'
    actualizarDatosPersonales = apiVersion + '/actualizarDatosPersonales'
    
    # Docente
    listarDocente = apiVersion + '/listarDocente'
    obtenerMateriasAsignadas = apiVersion + '/obtenerMateriasAsignadas'
    listarMateriaEstudianteCurso = apiVersion + '/listarMateriaEstudianteCurso'

    # Nota
    listarNota = apiVersion + '/listarNota'
    gestionarNota = apiVersion + '/gestionarNota'
    listarNotaEstudiante = apiVersion + '/listarNotaEstudiante'
    listarNotaDocente = apiVersion + '/listarNotaDocente'
    listarNotaEstudianteMateria = apiVersion + '/listarNotaEstudianteMateria'
    listarNotaEstudianteCurso = apiVersion + '/listarNotaEstudianteCurso'
    rptNotaEstudianteMateria = apiVersion + '/rptNotaEstudianteMateria'
    rptNotaCursoMateria = apiVersion + '/rptNotaCursoMateria'
    rptNotaCursoMateriaGeneral = apiVersion + '/rptNotaCursoMateriaGeneral'
    rptNotaCursoMateriaDocente = apiVersion + '/rptNotaCursoMateriaDocente'
    listarNotaCurso = apiVersion + '/listarNotaCurso'
    
    # Pago
    listarPago = apiVersion + '/listarPago'
    listarPagoEstudiante = apiVersion + '/listarPagoEstudiante'
    listarPagoEstudianteMateria = apiVersion + '/listarPagoEstudianteMateria'
    listarPagoEstudiantesMateria = apiVersion + '/listarPagoEstudiantesMateria'
    listarPagoCurso = apiVersion + '/listarPagoCurso'
    managePayment = apiVersion + '/managePayment'
    manageAssignPayment= apiVersion + '/manageAssignPayment'
    tipoPago = apiVersion + '/tipoPago'
    getPayments = apiVersion + '/getPayments'
    getPagoById = apiVersion + '/getPagoById/<int:pagid>'
    
    # Asistencia
    listarAsistencia = apiVersion + '/listarAsistencia'
    
    # Material de Apoyo
    getListTextoCombo = apiVersion + '/getListTextoCombo'
    
    # Reportes
    rptTotalesSigma = apiVersion + '/rptTotalesSigma'
    rptCursoMateriaContabilidad = apiVersion + '/rptCursoMateriaContabilidad'
    rptInformacionAdmision = apiVersion + '/rptInformacionAdmision'
    
    
    # Contabilidad
    listarCursoMateriaContabilidad = apiVersion + '/listarCursoMateriaContabilidad'
    getListCursoMateriaContabilidadById = apiVersion + '/getListCursoMateriaContabilidadById'
    
    
    #principal
    listarCantidades = apiVersion + '/listarCantidades'
    listarEstudiantesMateria = apiVersion + '/listarEstudiantesMateria'
    listarEstudiantesNivel = apiVersion + '/listarEstudiantesNivel'
    
    #Permiso
    listarPermiso = apiVersion + '/listarPermiso'
    listarPermisoRol = apiVersion + '/listarPermisoRol'
    getPermisos = apiVersion + '/getPermisos'
    
    getOperaciones = apiVersion + '/getOperaciones'
    updatePermiso = apiVersion + '/updatePermiso'
    addPermiso = apiVersion + '/addPermiso'
    deletePermiso = apiVersion + '/deletePermiso'
    
    
    #Operacion
    getTipoOperacion = apiVersion + '/getTipoOperacion'
    getOperations = apiVersion + '/getOperations'
    createOperation = apiVersion + '/createOperation'
    updateOperation = apiVersion + '/updateOperation/<int:opeid>'
    deleteOperation = apiVersion + '/deleteOperation/<int:opeid>'
    
    #Acceso
    getAccesos = apiVersion + '/getAccesses'
    getSubMenus = apiVersion + '/getSubMenus'
    getSubMenuType = apiVersion + '/getSubMenuType'
    createAccess = apiVersion + '/createAccess'
    updateAccess = apiVersion + '/updateAccess/<int:accid>'
    deleteAccess = apiVersion + '/deleteAccess/<int:accid>'
    getIconoNombre = apiVersion + '/getIconoNombre/<int:submenid>'
    
    #Menus
    getMenus = apiVersion + '/getMenus'
    createMenu = apiVersion + '/createMenu'
    updateMenu = apiVersion + '/updateMenu/<int:menid>'
    deleteMenu = apiVersion + '/deleteMenu/<int:menid>'
    
    #tipoIcono
    getTipoIcono = apiVersion + '/getTipoIcono'
    findIdIcono = apiVersion + '/findIdIcono'

    #SubMenu
    getTipoMenu = apiVersion + '/getTipoMenu'
    getListSubMenu = apiVersion + '/getListSubMenu'
    createSubMenu = apiVersion + '/createSubMenu'
    updateSubMenu = apiVersion + '/updateSubMenu/<int:submenid>'
    deleteSubMenu = apiVersion + '/deleteSubMenu/<int:submenid>'
    
    # Persona Información Personal
    informacionPersonal = apiVersion + '/informacionPersonal/<int:perid>'
    personaInformacionPersonal = apiVersion + '/informacionPersonal'
    
    # Persona Información Académica
    informacionAcademica = apiVersion + '/informacionAcademica/<int:perid>'
    informacionAcademicav2 = apiVersion + '/informacionAcademica/<int:perinfoaca>'
    personaInformacionAcademica = apiVersion + '/informacionAcademica'
    
    # Persona Información Ministerial
    informacionMinisterial = apiVersion + '/informacionMinisterial/<int:perid>'
    personaInformacionMinisterial = apiVersion + '/informacionMinisterial'
    personaInformacionMinisterialv2 = apiVersion + '/informacionMinisterial/<int:perinfomin>'
    
    # Persona Documento Admisión
    
    documentoAdmision = apiVersion + '/documentoAdmision/<int:perid>'
    personaDocumentoAdmision = apiVersion + '/documentoAdmision'
    personaDocumentoAdmisionv2 = apiVersion + '/documentoAdmision/<int:perdocadm>'
    documentoAdmisionv2 = apiVersion + '/documentoAdmision/<string:filename>'
    # Tipo Profesión
    tipoProfesion = apiVersion + '/tipoProfesion'
    tipoProfesionv2 = apiVersion + '/tipoProfesion/<int:proid>'
    
    # Tipo Educación
    tipoEducacion = apiVersion + '/tipoEducacion'
    tipoEducacionv2 = apiVersion + '/tipoEducacion/<int:eduid>'
    
    # Tipo Cargo
    tipoCargo = apiVersion + '/tipoCargo'
    tipoCargov2 = apiVersion + '/tipoCargo/<int:carid>'
    
    # Texto
    listTexto = apiVersion + '/getTextos'
    createTexto = apiVersion + '/createTexto'
    updateTexto = apiVersion + '/updateTexto/<int:texid>'
    deleteTexto = apiVersion + '/deleteTexto/<int:texid>'

    # TipoTexto
    listTipoTexto = apiVersion + '/getTipoTextos'
    createTipoTexto = apiVersion + '/createTipoTexto'
    updateTipoTexto = apiVersion + '/updateTipoTexto/<int:tiptexid>'
    deleteTipoTexto = apiVersion + '/deleteTipoTexto/<int:tiptexid>'

    # TipoIdiomaTexto
    listTipoIdiomaTexto = apiVersion + '/getTipoIdiomaTextos'
    createTipoIdiomaTexto = apiVersion + '/createTipoIdiomaTexto'
    updateTipoIdiomaTexto = apiVersion + '/updateTipoIdiomaTexto/<int:tipidiid>'
    deleteTipoIdiomaTexto = apiVersion + '/deleteTipoIdiomaTexto/<int:tipidiid>'

    # TipoCategoriaTexto
    listTipoCategoriaTexto = apiVersion + '/getTipoCategoriaTextos'
    createTipoCategoriaTexto = apiVersion + '/createTipoCategoriaTexto'
    updateTipoCategoriaTexto = apiVersion + '/updateTipoCategoriaTexto/<int:tipcatid>'
    deleteTipoCategoriaTexto = apiVersion + '/deleteTipoCategoriaTexto/<int:tipcatid>'

    # TipoExtensionTexto
    listTipoExtensionTexto = apiVersion + '/getTipoExtensionTextos'
    createTipoExtensionTexto = apiVersion + '/createTipoExtensionTexto'
    updateTipoExtensionTexto = apiVersion + '/updateTipoExtensionTexto/<int:tipextid>'
    deleteTipoExtensionTexto = apiVersion + '/deleteTipoExtensionTexto/<int:tipextid>'

    # MateriaTexto
    listMateriaTexto = apiVersion + '/getMateriaTextos'
    createMateriaTexto = apiVersion + '/createMateriaTexto'
    updateMateriaTexto = apiVersion + '/updateMateriaTexto/<int:mattexid>'
    deleteMateriaTexto = apiVersion + '/deleteMateriaTexto/<int:mattexid>'