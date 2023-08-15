# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from core.webd.lib import setup_db_trigger
from rs import db

from .lib import decrypt, encrypt

# -------------------------------------------------------------------------------------------------------------------- #

class Secret(db.DbObj):
    _table_name = 'rs.secret'
    _columns = ['id', 'key', 'value']
    _decoders = {'value': decrypt}
    _encoders = {'value': encrypt}

# -------------------------------------------------------------------------------------------------------------------- #


def init_tables(old_schema):

    current_schema = 1

    # XXX REMOVE BEFORE v1.0.0
    from rs import settings
    if settings.get('@rs.core.schema_version'):
        return current_schema
    if settings.get('@rs.schema_version.core.core'):
        return current_schema
    # XXX END REMOVE

    if old_schema < 1:
        db.query('''
            CREATE TABLE rs.secret (
                id      BIGSERIAL PRIMARY KEY,
                key     TEXT NOT NULL UNIQUE,
                value   TEXT NOT NULL
            );
        ''')
        setup_db_trigger('rs.secret')

    return current_schema

# -------------------------------------------------------------------------------------------------------------------- #
