from aiohttp import web
from aiohttp_apispec import request_schema

from .schemas import LoadBodyData
from .utils import json_response
from api.utils import get_anagrams_dict
from api.utils import sort

__all__ = ['index', 'load', 'get']


async def index(request: web.Request) -> web.Response:
    return web.HTTPOk()


async def get(request: web.Request) -> web.Response:
    null_response_data = None
    try:
        word = sort(request.query['word'])
    except KeyError:
        return json_response(null_response_data)

    with await request.app.get('redis-pool') as conn:
        redis_response_data = await conn.execute('SMEMBERS', word, encoding='utf-8')
        if redis_response_data:
            return json_response(redis_response_data)
    return json_response(null_response_data)


@request_schema(LoadBodyData)
async def load(request: web.Request) -> web.Response:
    request_body_data = await request.json()
    anagrams_dict = get_anagrams_dict(request_body_data['words'])

    with await request.app.get('redis-pool') as conn:
        for key, values in anagrams_dict.items():
            await conn.execute('SADD', key, *values)
    return web.HTTPOk()
