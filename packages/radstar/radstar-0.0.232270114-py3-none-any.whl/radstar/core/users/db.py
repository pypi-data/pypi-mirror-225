# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import bcrypt

from core.webd.lib import setup_db_trigger
from rs import db

BCRYPT_ROUNDS = 9

# -------------------------------------------------------------------------------------------------------------------- #

class User(db.DbObj):
    _table_name = 'rs.user'
    _columns = ['id', 'uid', 'name', 'password', 'super_user', 'data']
    _encoders = {
        'data': db.Jsonb,
        'password': lambda x: bcrypt.hashpw(x.encode(), bcrypt.gensalt(BCRYPT_ROUNDS)),
    }

# -------------------------------------------------------------------------------------------------------------------- #


def init_tables(old_schema):

    current_schema = 1


    if old_schema < 1:
        db.query('''
            CREATE TABLE rs.user (
                id              BIGSERIAL PRIMARY KEY,
                uid             TEXT UNIQUE NOT NULL,
                name            TEXT NOT NULL DEFAULT '',
                password        BYTEA,
                super_user      BOOLEAN NOT NULL DEFAULT FALSE,
                data            JSONB NOT NULL DEFAULT '{}'
            );
        ''')
        setup_db_trigger('rs.user')

        # create initial admin user
        User.insert(uid='admin', name='admin', password='admin', super_user=True)


    return current_schema

# -------------------------------------------------------------------------------------------------------------------- #
