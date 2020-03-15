from aiohttp import web

from api.views import *


def setup_routes(app: web.Application) -> None:
    app.router.add_get('/', index)
    app.router.add_get('/get', get)
    app.router.add_post('/load', load)
