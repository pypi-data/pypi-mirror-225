# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from contextlib import contextmanager
from datetime import timedelta
from functools import partial
from typing import Any
import asyncio
import threading
import time
import traceback

from psycopg.pq import TransactionStatus
import psycopg
import psycopg_pool

from . import AsIs
from ..utils import getenv

# -------------------------------------------------------------------------------------------------------------------- #

DEFAULT_CONNINFO = 'host=postgres dbname=rs user=rs password=rs'
MIN_CONNECTIONS = 2
MAX_CONNECTIONS = 4

_thread_data = threading.local()
_lock = threading.Lock()

# -------------------------------------------------------------------------------------------------------------------- #

def get_conninfo():
    return getenv('RS_DB_CONNINFO', DEFAULT_CONNINFO)

# -------------------------------------------------------------------------------------------------------------------- #

def get_connopts(**options):
    return {
        'cursor_factory': psycopg.ClientCursor,
        'row_factory': row_factory,
        **options
    }

# -------------------------------------------------------------------------------------------------------------------- #

def init_db(min_connections=MIN_CONNECTIONS, max_connections=MAX_CONNECTIONS, **options):
    # pylint: disable=global-variable-undefined
    global _pool
    _pool = psycopg_pool.ConnectionPool(
        conninfo=get_conninfo(),
        min_size=min(min_connections, max_connections),
        max_size=max(min_connections, max_connections),
        kwargs=get_connopts(**options),
    )

# -------------------------------------------------------------------------------------------------------------------- #

def init_tables(app_name, callback=None):

    from .. import settings

    # create radstar schema and setting table
    query('''\
        CREATE SCHEMA IF NOT EXISTS rs;

        CREATE TABLE IF NOT EXISTS rs.setting (
            key         TEXT NOT NULL UNIQUE,
            value       JSONB NOT NULL
        );
    ''')

    if callback is None:
        return

    # get current schema version
    schema_settings_name = f'@rs.schema_version.{app_name}'
    current_schema = settings.get(schema_settings_name, 0)

    # init tables
    new_schema = callback(current_schema)

    # update schema version if needed
    if new_schema != current_schema:
        settings.set(schema_settings_name, new_schema)

# -------------------------------------------------------------------------------------------------------------------- #

def query(query_, binary_=False, **kw):
    cur = _thread_data.conn.cursor(binary=binary_)
    cur.execute(query_, kw)
    return cur

# -------------------------------------------------------------------------------------------------------------------- #

class Row(dict):

    def __init__(self, fields, values):
        super().__init__(zip(fields, values))
        self._value_list = values

    def __getitem__(self, items):
        if isinstance(items, (int, slice)):
            return self._value_list[items]
        return super().__getitem__(items)


def row_factory(cursor: psycopg.Cursor[Any] | None) -> psycopg.rows.RowMaker[dict[str, Any]]:
    if cursor.description is None:
        return None
    return partial(Row, [x.name for x in cursor.description])

# -------------------------------------------------------------------------------------------------------------------- #

@contextmanager
def transaction(*, use_pool: bool=True):

    conn = getattr(_thread_data, 'conn', None)
    if conn is not None:
        with conn.transaction():
            yield conn
        return

    _thread_data.conn = conn = _get_conn_from_pool() if use_pool is True \
            else psycopg.connect(get_conninfo(), **get_connopts())
    try:
        yield conn
    except:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        if use_pool is True:
            _pool.putconn(conn)
        del _thread_data.conn


def _get_conn_from_pool():

    backoff = 0.0

    for _ in range(20):

        conn = _pool.getconn()
        try:
            conn.execute('SELECT 1')
            if conn.pgconn.transaction_status != TransactionStatus.UNKNOWN:
                return conn
        except:
            traceback.print_exc() # XXX
            _pool.putconn(conn)

        if _lock.acquire(blocking=False) is True:
            try:
                _pool.check()
            finally:
                _lock.release()

        time.sleep(backoff)
        backoff += 0.1

# -------------------------------------------------------------------------------------------------------------------- #

def now(*, add=None, sub=None):

    s = 'CURRENT_TIMESTAMP'

    if add is not None:
        if isinstance(add, (int, float)):
            add = timedelta(seconds=add)
        s += f' + {psycopg.sql.quote(add)}'

    if sub is not None:
        if isinstance(sub, (int, float)):
            sub = timedelta(seconds=sub)
        s += f' - {psycopg.sql.quote(sub)}'

    return AsIs(s)

# -------------------------------------------------------------------------------------------------------------------- #

async def to_thread(func, *a, **kw):
    def with_transaction():
        with transaction():
            return func(*a, **kw)
    return await asyncio.to_thread(with_transaction)

# -------------------------------------------------------------------------------------------------------------------- #
