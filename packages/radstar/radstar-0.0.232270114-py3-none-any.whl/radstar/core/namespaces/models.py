# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=abstract-method

# -------------------------------------------------------------------------------------------------------------------- #

from html import escape
from typing import Any, Optional

from core.webd.lib import BaseModel, DbObjModel, model, Notification, user_var
from rs.db import query

from . import db # pylint: disable=no-name-in-module
from .lib import NamespaceDbObjModel, get_ns_id

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.NamespaceOptions')
class NamespaceOptions(BaseModel):

    read_permissions = 'user'

    def list(self, limit: Optional[int], offset: Optional[int], filters: dict) -> Any:
        # NOTE: always include all results (no limit/offset)
        user = user_var.get()
        return query('''\
            SELECT DISTINCT namespace.id, namespace.uid, namespace.name FROM rs.namespace
            FULL JOIN rs.member ON namespace.id = member.namespace_id
            WHERE member_id = %(user_id)s OR namespace.id = %(user_id)s OR namespace.id = %(ns_id)s
            ORDER BY namespace.uid NULLS LAST, namespace.name
        ''', user_id=user.id, ns_id=user.ns_id)

    def transform(self, x: Any) -> dict:
        # automatically html encode the name
        name = f'@{x["uid"]}' if x['uid'] else f'#{x["name"]}'
        return {'id': x['id'], 'value': escape(name)}

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.Namespace')
class Namespace(BaseModel):

    def notify_prepare(self, notification: Notification) -> None:
        for m in ['rs.User', 'rs.Namespace']:
            notification.add_extra(m, notification.event, notification.id)
        notification.skip = True

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.User')
class User(DbObjModel):

    read_permissions = 'super_user'
    write_permissions = 'super_user'
    delete_permissions = 'super_user'

    dbobj = db.Namespace
    what = ['id', 'uid', 'name', 'super_user']
    uid_where = 'UID IS NOT NULL'

    def get(self, id: int) -> Any:
        return self.dbobj.get(where=f'id = {id:d} AND {self.uid_where}', what=','.join(self.what))

    def list(self, limit: Optional[int], offset: Optional[int], filters: dict) -> Any:
        # TODO: implement sorting
        where, vars = self.process_filters(filters)
        return self.dbobj.iter(
            what=','.join(self.what),
            where=f'{self.uid_where} AND {where}', vars=vars,
            limit=limit, offset=offset
        )

    def count(self, filters: dict) -> Optional[int]:
        where, vars = self.process_filters(filters)
        return query(f'SELECT COUNT(*) FROM {self.dbobj._table_name} WHERE {self.uid_where} AND {where}',
                **vars).fetchone()[0]

    def validate_data(self, id: Optional[int], data: dict) -> dict:
        d = {
            'uid': data['uid'],
            'name': data['name'],
            'super_user': bool(data.get('super_user', False)),
        }
        if pw := data.get('password'):
            d['password'] = pw
        elif id is None:
            raise Exception('missing password')
        return d

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.Namespace')
class Namespace(User):

    what = ['id', 'name']
    uid_where = 'UID IS NULL'

    def validate_data(self, id: Optional[int], data: dict) -> dict:
        return {'name': data['name']}

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.Member')
class Member(NamespaceDbObjModel):

    read_permissions = 'user'
    write_permissions = 'ns_admin'
    delete_permissions = 'ns_admin'

    dbobj = db.Member

    def get(self, id: int) -> Any:
        return query(f'''\
            SELECT m.id, m.namespace_id, ns.uid, ns.name, m.admin FROM rs.member m
            JOIN rs.namespace ns ON m.member_id = ns.id
            WHERE m.id = {id:d}
        ''').fetchone()

    notify_get = get

    def list(self, limit: Optional[int], offset: Optional[int], filters: dict) -> Any:
        # TODO: implement sorting
        where, vars = self.process_filters(filters)
        return query(f'''\
            SELECT m.id, ns.uid, ns.name, m.admin FROM rs.member m
            JOIN rs.namespace ns ON m.member_id = ns.id
            WHERE {where} AND m.namespace_id = {get_ns_id():d}
            ORDER BY ns.name
            LIMIT {limit:d} OFFSET {offset:d}
        ''', **vars)

    def validate_data(self, id: Optional[int], data: dict) -> dict:
        # pylint: disable=unused-argument
        user_ns = db.Namespace.get(what='id', where='uid = %(uid)s', vars={'uid': data['uid']})
        if user_ns is None:
            raise Exception('invalid user')
        return {
            'member_id': user_ns.id,
            'admin': bool(int(data['admin']))
        }

# -------------------------------------------------------------------------------------------------------------------- #
