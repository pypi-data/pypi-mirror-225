# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from concurrent.futures import ThreadPoolExecutor
import asyncio

import aiohttp
import click
import rs

from . import app, routes
from . import auth, websocket # pylint: disable=unused-import

# -------------------------------------------------------------------------------------------------------------------- #

LISTEN_HOST = '127.0.0.1'
LISTEN_PORT = 5001
MAX_THREADS = 8

# -------------------------------------------------------------------------------------------------------------------- #

@click.command()
@click.option('--host', help='Listen host.', default=LISTEN_HOST)
@click.option('--port', help='Listen port.', default=LISTEN_PORT, type=int)
@click.option('--path', help='Unix domain socket path.')
@click.option('--threads', help='Max threads.', default=MAX_THREADS, type=int)
def main(host, port, path, threads):

    # init db
    rs.db.init_db(max_connections=threads)

    # init radstar
    rs.init(['models', 'rpc', 'web'])

    # code to run once the asyncio loop has started
    async def on_startup(_):

        # create default thread pool executor
        asyncio.get_running_loop().set_default_executor(ThreadPoolExecutor(max_workers=threads))

        # init notifications
        from .notify import init_notifications
        init_notifications(conninfo=rs.db.get_conninfo())

    app.on_startup.append(on_startup)

    # cleanly shutdown websockets
    app['websockets'] = {}
    async def shutdown_websockets(a):
        for ws in list(a['websockets']):
            await ws.close()
    app.on_shutdown.append(shutdown_websockets)

    # register routes
    app.router.add_routes(routes)

    # run app
    if path is not None:
        aiohttp.web.run_app(app, path=path)
    else:
        aiohttp.web.run_app(app, host=host, port=port)

# -------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter

# -------------------------------------------------------------------------------------------------------------------- #
