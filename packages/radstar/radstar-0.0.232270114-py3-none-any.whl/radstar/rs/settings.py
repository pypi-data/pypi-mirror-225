# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from .db import Jsonb, query

# -------------------------------------------------------------------------------------------------------------------- #

def get(key, default=None):
    value = query('SELECT value FROM rs.setting WHERE key = %(key)s', key=key).fetchone()
    return value[0] if value is not None else default

# -------------------------------------------------------------------------------------------------------------------- #

def set(key, value):
    # pylint: disable=redefined-builtin
    query('''\
        INSERT INTO rs.setting (key, value) VALUES (%(key)s, %(value)s)
        ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
    ''', key=key, value=Jsonb(value))

# -------------------------------------------------------------------------------------------------------------------- #
