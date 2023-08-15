# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import asyncio
import traceback

from rs import db, json, plugins
import psycopg

from . import app

# -------------------------------------------------------------------------------------------------------------------- #

class Notification:

    def __init__(self, model_name: str, event: str, id: int):

        model = plugins.get('core.webd.model', model_name)
        if model is None:
            raise Exception(f'invalid model: {model_name}')

        self.model_name = model_name
        self.model = model()
        self.event = event
        self.id = id
        self.data = {}
        self.extras = []
        self.skip = False

    def add_extra(self, model: str, event: str, id: int) -> None:
        self.extras.append(Notification(model, event, id))

# -------------------------------------------------------------------------------------------------------------------- #

def setup_db_trigger(table_name):
    db.query(f'''\
        CREATE TRIGGER {table_name.replace('.', '__')}_webd_trigger
        BEFORE INSERT OR UPDATE OR DELETE
        ON {table_name}
        FOR EACH ROW EXECUTE PROCEDURE rs.webd_modify_trigger()
    ''')

# -------------------------------------------------------------------------------------------------------------------- #

def init_notifications(**conn_info):

    task = asyncio.get_running_loop().create_task(_pg_listen(conn_info))

    async def shutdown(_):
        task.cancel()
        await task

    app.on_shutdown.append(shutdown)

# -------------------------------------------------------------------------------------------------------------------- #

async def _pg_listen(conn_info):

    while True:

        try:
            async with await psycopg.AsyncConnection.connect(**conn_info, autocommit=True) as conn:

                async with conn.cursor() as cur:

                    await cur.execute('LISTEN "rs.webd"')
                    gen = conn.notifies()

                    async for msg in gen:
                        try:
                            schema, table, operation, row_id = msg.payload.split('|')
                            if schema != 'public':
                                table = f'{schema}.{table}'
                            model_name = plugins.get('core.webd.model_from_table', table)
                            if model_name:
                                await _handle_notification(Notification(model_name, operation.lower(), int(row_id)))
                        except:
                            traceback.print_exc() # XXX

        except asyncio.exceptions.CancelledError:
            return

        except:
            traceback.print_exc() # XXX

        await asyncio.sleep(0.5)

# -------------------------------------------------------------------------------------------------------------------- #

async def _handle_notification(notification: Notification):

    # call model to update notification data and extras
    await db.to_thread(notification.model.notify_prepare, notification)

    # handle extra notifications
    for n in notification.extras:
        await _handle_notification(n)

    # skip this notification?
    if notification.skip is True:
        return

    # prepare data to send
    data_to_send = json.dumps({
        'event': notification.event,
        'id': notification.id,
        'model': notification.model_name,
        'data': notification.data
    })

    # iterate websockets and send the event to subscribers with access
    for ws, ws_data in list(app['websockets'].items()):
        if not ws_data['sub'].get(notification.model_name, False):
            continue
        if await notification.model.notify_has_access(notification, ws_data['user']) is True:
            await ws.send_str(data_to_send)

# -------------------------------------------------------------------------------------------------------------------- #
