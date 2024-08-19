from flask_restful import Api
import resources.Texto_resource as Texto
from client.routes import Routes as routes

def texto_routes(api: Api):
    # Rutas para Texto
    api.add_resource(Texto.GetListTexto, routes.listTexto)
    api.add_resource(Texto.CreateTexto, routes.createTexto)
    api.add_resource(Texto.UpdateTexto, routes.updateTexto)
    api.add_resource(Texto.DeleteTexto, routes.deleteTexto)

    # Rutas para TipoTexto
    api.add_resource(Texto.GetListTipoTexto, routes.listTipoTexto)
    api.add_resource(Texto.CreateTipoTexto, routes.createTipoTexto)
    api.add_resource(Texto.UpdateTipoTexto, routes.updateTipoTexto)
    api.add_resource(Texto.DeleteTipoTexto, routes.deleteTipoTexto)

    # Rutas para TipoIdiomaTexto
    api.add_resource(Texto.GetListTipoIdiomaTexto, routes.listTipoIdiomaTexto)
    api.add_resource(Texto.CreateTipoIdiomaTexto, routes.createTipoIdiomaTexto)
    api.add_resource(Texto.UpdateTipoIdiomaTexto, routes.updateTipoIdiomaTexto)
    api.add_resource(Texto.DeleteTipoIdiomaTexto, routes.deleteTipoIdiomaTexto)

    # Rutas para TipoCategoriaTexto
    api.add_resource(Texto.GetListTipoCategoriaTexto, routes.listTipoCategoriaTexto)
    api.add_resource(Texto.CreateTipoCategoriaTexto, routes.createTipoCategoriaTexto)
    api.add_resource(Texto.UpdateTipoCategoriaTexto, routes.updateTipoCategoriaTexto)
    api.add_resource(Texto.DeleteTipoCategoriaTexto, routes.deleteTipoCategoriaTexto)

    # Rutas para TipoExtensionTexto
    api.add_resource(Texto.GetListTipoExtensionTexto, routes.listTipoExtensionTexto)
    api.add_resource(Texto.CreateTipoExtensionTexto, routes.createTipoExtensionTexto)
    api.add_resource(Texto.UpdateTipoExtensionTexto, routes.updateTipoExtensionTexto)
    api.add_resource(Texto.DeleteTipoExtensionTexto, routes.deleteTipoExtensionTexto)

    # Rutas para MateriaTexto
    api.add_resource(Texto.GetListMateriaTexto, routes.listMateriaTexto)
    api.add_resource(Texto.CreateMateriaTexto, routes.createMateriaTexto)
    api.add_resource(Texto.UpdateMateriaTexto, routes.updateMateriaTexto)
    api.add_resource(Texto.DeleteMateriaTexto, routes.deleteMateriaTexto)
