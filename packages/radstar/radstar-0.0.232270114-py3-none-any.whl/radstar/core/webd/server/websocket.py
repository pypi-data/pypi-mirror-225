# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import asyncio
import traceback

from rs import db, json, plugins
import aiohttp

from . import app, auth, routes

# -------------------------------------------------------------------------------------------------------------------- #

@routes.get('/_ws')
async def ws_handler(request):

    ws = aiohttp.web.WebSocketResponse(heartbeat=30.0)
    await ws.prepare(request)

    app['websockets'][ws] = {'sub': {}, 'user': None}
    try:

        state = 'hello'

        # main loop
        async for msg in ws:
            if msg.type != aiohttp.WSMsgType.TEXT:
                continue

            op = _Operation.decode(msg.data)
            if not op:
                continue

            #
            # hello/login
            #

            if state == op.operation == 'hello':
                hello_data = op.data
                state = 'login'

            elif state == op.operation == 'login':
                user = await asyncio.to_thread(_authenticate, op)
                if user is None:
                    await _reply(ws, op, error='login failed')
                else:
                    auth.user_var.set(user)
                    app['websockets'][ws]['user'] = user

                    welcome_data = await asyncio.to_thread(_welcome, user, hello_data)
                    await _reply(ws, op, status='welcome', data=welcome_data)

                    state = 'authenticated'
                    continue

            if state == 'login':
                await _reply(ws, op, status='login-required')

            #
            # authenticated operations
            #

            if state != 'authenticated':
                continue

            # subscribe to / unsubscribe from model update notifications
            if op.operation in ('subscribe', 'unsubscribe'):
                app['websockets'][ws]['sub'][op.model] = op.operation == 'subscribe'
                await _reply(ws, op, data=True)
                continue

            # call handler
            try:
                data = await asyncio.to_thread(_get_and_run_handler, op)
                await _reply(ws, op, data=data)
            except Exception as e:
                traceback.print_exc()
                await _reply(ws, op, error=str(e))

    finally:
        del app['websockets'][ws]
        await ws.close()

    return ws

# -------------------------------------------------------------------------------------------------------------------- #

class _Operation:

    def __init__(self, **kw):
        self.operation = kw['operation']
        self.call_id = kw.get('call_id')
        self.data = kw.get('data') or {}
        self.model = kw.get('model')

    @staticmethod
    def decode(msg_data):
        try:
            return _Operation(**json.loads(msg_data))
        except:
            return None

# -------------------------------------------------------------------------------------------------------------------- #

async def _reply(ws, op, *, status='success', data=None, error=None):

    response = {
        'status': status
    }

    if op.call_id is not None:
        response['call_id'] = op.call_id

    if data is not None:
        response['data'] = data

    if error is not None:
        response['status'] = 'error'
        response['error'] = error

    await ws.send_str(json.dumps(response))

# -------------------------------------------------------------------------------------------------------------------- #

def _authenticate(op):

    username = op.data.get('username')
    password = op.data.get('password')
    if not username or not password:
        return None

    return auth.get_auth_plugin().authenticate(username, password)

# -------------------------------------------------------------------------------------------------------------------- #

def _welcome(user, hello_data):
    return auth.get_auth_plugin().welcome(user, hello_data)

# -------------------------------------------------------------------------------------------------------------------- #

def _get_and_run_handler(op):

    # get model
    model = plugins.get('core.webd.model', op.model)
    if model is None:
        raise Exception('invalid model')

    # get handler
    handler = getattr(model(), f'rs_{op.operation}', None)
    if handler is None:
        raise Exception('invalid handler')

    # run handler
    if getattr(handler, 'transaction', True) is True:
        with db.transaction():
            return handler(**op.data)
    else:
        return handler(**op.data)

# -------------------------------------------------------------------------------------------------------------------- #
