from collections import defaultdict
from typing import Union

import ujson
from aiohttp import web


def json_response(data: Union[list, None], **kwargs) -> web.Response:
    kwargs.setdefault('headers', {'content-type': 'application/json'})
    return web.Response(body=ujson.dumps(data, ensure_ascii=False), **kwargs)


def sort(word: str) -> str:
    return ''.join(sorted(word.lower().strip()))


def get_anagrams_dict(words: list) -> defaultdict:
    dd = defaultdict(set)
    for w in words:
        key = sort(w)
        dd[key].add(w)
    return dd
