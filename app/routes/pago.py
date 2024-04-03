from flask_restful import Api
import resources.Pago as Pago
from client.routes import Routes as routes

def pago_routes(api: Api):
    api.add_resource(Pago.ListarPago, routes.listarPago)
    api.add_resource(Pago.ListarPagoEstudiante, routes.listarPagoEstudiante)
    api.add_resource(Pago.ListarPagoEstudianteMateria, routes.listarPagoEstudianteMateria)
    api.add_resource(Pago.ListarPagoEstudiantesMateria, routes.listarPagoEstudiantesMateria)
    api.add_resource(Pago.ListarPagoCurso, routes.listarPagoCurso)
    api.add_resource(Pago.GestionarPago, routes.gestionarPago)
    api.add_resource(Pago.TipoPago, routes.tipoPago)
    api.add_resource(Pago.GetPayments, routes.getPayments)
    api.add_resource(Pago.InsertarPago, routes.insertarPago)
    api.add_resource(Pago.AsignarPagoInscripcion, routes.asignarPagoInscripcion)
    api.add_resource(Pago.ObtenerUltimoPago, routes.obtenerUltimoPago)
    api.add_resource(Pago.ModificarPago, routes.modificarPago)