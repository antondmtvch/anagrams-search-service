from aiohttp import web
from aiohttp_apispec import request_schema

from .schemas import LoadBodyData
from .utils import json_response
from api.utils import get_anagrams_dict
from api.utils import sort

__all__ = ['index', 'load', 'get']


async def index(request: web.Request)-> web.Response:
    return web.HTTPOk()


async def get(request: web.Request)-> web.Response:
    if not request.query:
        return json_response(None)
    try:
        word = sort(request.query['word'])
    except KeyError:
        return web.HTTPBadRequest()

    with await request.app.get('redis-pool') as conn:
        data = await conn.execute('SMEMBERS', word, encoding='utf-8')
        if not data:
            return json_response(None)
    return json_response(data)


@request_schema(LoadBodyData)
async def load(request: web.Request) -> web.Response:
    body = await request.json()
    redis_data = get_anagrams_dict(body['words'])

    with await request.app.get('redis-pool') as conn:

        for k, v in redis_data.items():
            await conn.execute('SADD', k, *v)
    return web.HTTPOk()
