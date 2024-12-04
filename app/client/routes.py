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