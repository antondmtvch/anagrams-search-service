from collections import defaultdict
from typing import Union

import ujson
from aiohttp import web


def json_response(data: Union[list, None], **kwargs) -> web.Response:
    kwargs.setdefault(
        'headers',
        {
            'content-type': 'application/json'
        }
    )
    return web.Response(body=ujson.dumps(data, ensure_ascii=False), **kwargs)


def sort(word: str) -> str:
    return ''.join(sorted(word.lower().strip()))


def get_anagrams_dict(words: list) -> defaultdict:
    _dict = defaultdict(set)
    for word in words:
        key = sort(word)
        _dict[key].add(word)
    return _dict
