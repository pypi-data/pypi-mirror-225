# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import bcrypt

from core.webd.lib import setup_db_trigger
from rs import db

BCRYPT_ROUNDS = 9

# -------------------------------------------------------------------------------------------------------------------- #

class Namespace(db.DbObj):
    _table_name = 'rs.namespace'
    _columns = ['id', 'uid', 'name', 'password', 'super_user', 'data']
    _encoders = {
        'data': db.Jsonb,
        'password': lambda x: bcrypt.hashpw(x.encode(), bcrypt.gensalt(BCRYPT_ROUNDS)),
    }

class Member(db.DbObj):
    _table_name = 'rs.member'
    _columns = ['id', 'namespace_id', 'member_id', 'admin', 'data']
    _encoders = {
        'data': db.Jsonb,
    }

# -------------------------------------------------------------------------------------------------------------------- #


def init_tables(old_schema):

    current_schema = 2


    if old_schema == 0:
        db.query('''
            CREATE TABLE rs.namespace (
                id              BIGSERIAL PRIMARY KEY,
                uid             TEXT,
                name            TEXT NOT NULL,
                password        BYTEA,
                super_user      BOOLEAN NOT NULL DEFAULT FALSE,
                data            JSONB NOT NULL DEFAULT '{}'
            );
            CREATE UNIQUE INDEX ON rs.namespace (name) WHERE uid IS NULL;
            CREATE UNIQUE INDEX ON rs.namespace (uid) WHERE uid IS NOT NULL;

            CREATE TABLE rs.member (
                id              BIGSERIAL PRIMARY KEY,
                namespace_id    BIGINT REFERENCES rs.namespace (id) ON DELETE CASCADE NOT NULL,
                member_id       BIGINT REFERENCES rs.namespace (id) ON DELETE CASCADE NOT NULL,
                admin           BOOLEAN NOT NULL DEFAULT FALSE,
                data            JSONB NOT NULL DEFAULT '{}'
            );
            CREATE UNIQUE INDEX ON rs.member (namespace_id, member_id);
        ''')
        for tbl in ['rs.namespace', 'rs.member']:
            setup_db_trigger(tbl)

        # create initial admin user
        Namespace.insert(uid='admin', name='admin', password='admin', super_user=True)


    return current_schema

# -------------------------------------------------------------------------------------------------------------------- #
