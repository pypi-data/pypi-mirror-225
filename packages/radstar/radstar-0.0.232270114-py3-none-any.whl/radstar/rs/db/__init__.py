# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=wrong-import-position

# -------------------------------------------------------------------------------------------------------------------- #

from psycopg.types.json import Jsonb
import psycopg

# -------------------------------------------------------------------------------------------------------------------- #

# NOTE: this only works for ClientCursor() cursors

class AsIs(str):
    ...

class AsIsDumper(psycopg.adapt.Dumper):
    def dump(self, obj: AsIs) -> bytes:
        return obj.encode('ascii')
    quote = dump

psycopg.adapters.register_dumper(AsIs, AsIsDumper)

# -------------------------------------------------------------------------------------------------------------------- #

from .. import json
psycopg.types.json.set_json_dumps(json.dumps)
psycopg.types.json.set_json_loads(json.loads)

# -------------------------------------------------------------------------------------------------------------------- #

from .dbobj import DbObj
from .funcs import get_conninfo, get_connopts, init_db, init_tables, now, query, to_thread, transaction

# -------------------------------------------------------------------------------------------------------------------- #
