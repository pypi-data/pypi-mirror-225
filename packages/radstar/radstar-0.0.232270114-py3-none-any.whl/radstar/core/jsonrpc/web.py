# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from contextvars import ContextVar
from json.decoder import JSONDecodeError
import asyncio
import logging

from aiohttp import web

from core.webd.lib import routes
from rs import db, json, plugins

from .lib import PLUGIN_KEY, RPCError

# -------------------------------------------------------------------------------------------------------------------- #

VERSION = '2.0'

ERROR_CODES = {
    -32700: 'parse error',
    -32600: 'invalid request',
    -32601: 'method not found',
    -32602: 'invalid params',
    -32603: 'internal error',
}

# -------------------------------------------------------------------------------------------------------------------- #

@routes.post('/_jsonrpc')
async def rpc_handler(request: web.Request) -> web.StreamResponse:

    try:
        data = await request.json(loads=json.loads)
    except JSONDecodeError:
        return web.json_response(_error(-32700))

    _request_var.set(request)

    if isinstance(data, dict):
        response = await asyncio.to_thread(_call, data)
    elif isinstance(data, list):
        response = [await asyncio.to_thread(_call, x) for x in data]
    else:
        response = _error(-32600)

    return web.json_response(response, dumps=json.dumps)

# -------------------------------------------------------------------------------------------------------------------- #

def _call(data: dict) -> dict:

    if data.get('jsonrpc') != VERSION:
        return _error(-32600)
    id = data.get('id')

    method = data.get('method')
    if method is None:
        return _error(-32600, id=id)

    params = data.get('params')
    if params is None:
        args, kw = (), {}
    elif isinstance(params, list):
        args, kw = params, {}
    elif isinstance(params, dict):
        args, kw = (), params
    else:
        return _error(-32602, id=id)

    handler = plugins.get(PLUGIN_KEY, method)
    if handler is None:
        return _error(-32601, id=id)

    try:
        if getattr(handler, 'transaction', True) is True:
            with db.transaction():
                result = handler(*args, **kw)
        else:
            result = handler(*args, **kw)
    except RPCError as e:
        return _error(e.code, msg=e.msg, id=id)
    except:
        logging.warning(f'jsonrpc error {method=}', exc_info=True)
        return _error(-32603, id=id)

    return {
        'jsonrpc': VERSION,
        'result': result,
        'id': id,
    }

# -------------------------------------------------------------------------------------------------------------------- #

def _error(code, *, msg='error', id=None) -> dict:
    return {
        'jsonrpc': VERSION,
        'error': {
            'code': code,
            'message': ERROR_CODES.get(code, msg),
        },
        'id': id,
    }

# -------------------------------------------------------------------------------------------------------------------- #

def rpc_get_request() -> web.Request:
    return _request_var.get()

_request_var = ContextVar('current_request')

# -------------------------------------------------------------------------------------------------------------------- #
