# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from typing import Any, Optional

from core.webd.lib import DbObjModel, Notification, User, user_var
from rs import db

from .web import NamespaceUser

# -------------------------------------------------------------------------------------------------------------------- #

class NamespaceDbObjModel(DbObjModel):

    def get(self, id: int) -> Any:
        return self.dbobj.get(where=f'id = {id:d} AND namespace_id = {get_ns_id():d}', what=','.join(self.what))


    def list(self, limit: Optional[int], offset: Optional[int], filters: dict) -> Any:
        where, vars = self.process_filters(filters)
        return self.dbobj.iter(
            what=','.join(self.what),
            where=f'namespace_id = {get_ns_id():d} AND {where}', vars=vars,
            limit=limit, offset=offset
        )


    def count(self, filters: dict) -> Optional[int]:
        where, vars = self.process_filters(filters)
        return db.query(f'SELECT COUNT(*) FROM {self.dbobj._table_name} WHERE '
                f'namespace_id = {get_ns_id():d} AND {where}', **vars).fetchone()[0]


    def insert(self, data: dict) -> Any:
        return self.dbobj.insert(namespace_id=get_ns_id(), **data)


    def update(self, id: int, data: dict) -> Any:
        return db.query(f'''\
            UPDATE {self.dbobj._table_name} SET
            {', '.join(f'{k} = %({k})s' for k in data if k in self.dbobj._columns)}
            WHERE {self.dbobj._id_column} = {id:d} AND namespace_id = {get_ns_id():d}
            RETURNING {','.join(self.what)}
        ''', **{k: self.dbobj._encode(k, v) for k, v in data.items() if k in self.dbobj._columns}).fetchone()


    def delete(self, id: int) -> bool:
        r = db.query(f'''\
            DELETE FROM {self.dbobj._table_name}
            WHERE {self.dbobj._id_column} = {id:d} AND namespace_id = {get_ns_id():d}
        ''')
        return bool(r.rowcount)


    def notify_get(self, id: int) -> Any:
        return self.dbobj.get_by_id(id, what=','.join(self.what))


    async def notify_has_access(self, notification: Notification, user: Optional[User]) -> bool:

        if user is None:
            return False
        assert isinstance(user, NamespaceUser)

        if notification.event != 'delete':
            ns_id = notification.data.get('namespace_id')
            if not ns_id or user.ns_id != ns_id:
                return False

        return await super().notify_has_access(notification, user)

# -------------------------------------------------------------------------------------------------------------------- #

def get_ns_id() -> int:
    ''' return namespace id of currently logged in user. '''
    user = user_var.get()
    assert isinstance(user, NamespaceUser)
    return int(user.ns_id)

# -------------------------------------------------------------------------------------------------------------------- #
