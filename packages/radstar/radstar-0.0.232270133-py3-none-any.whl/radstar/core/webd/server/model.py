# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from typing import Any, List, Optional, Tuple

from rs import camel_to_snake, db, plugins

from .auth import User, user_var
from .notify import Notification

# -------------------------------------------------------------------------------------------------------------------- #

class BaseModel:

    read_permissions = None
    write_permissions = None
    delete_permissions = None

    # ---------------------------------------------------------------------------------------------------------------- #

    def get(self, id: int) -> Any:
        raise NotImplementedError()

    def list(self, limit: int, offset: int, filters: dict) -> Any:
        raise NotImplementedError()

    def count(self, filters: dict) -> Optional[int]:
        # pylint: disable=unused-argument
        return None

    def insert(self, data: dict) -> Any:
        raise NotImplementedError()

    def update(self, id: int, data: dict) -> Any:
        raise NotImplementedError()

    def delete(self, id: int) -> bool:
        raise NotImplementedError()

    def transform(self, x: Any) -> dict:
        return dict(x)

    def validate_data(self, id: Optional[int], data: dict) -> dict:
        # pylint: disable=unused-argument
        return data

    # ---------------------------------------------------------------------------------------------------------------- #

    def notify_get(self, id: int) -> Any:
        return self.get(id)


    def notify_prepare(self, notification: Notification) -> None:
        if notification.event != 'delete':
            x = self.notify_get(notification.id)
            if x is None:
                notification.skip = True
            else:
                notification.data = self.transform(x)


    async def notify_has_access(self, notification: Notification, user: Optional[User]) -> bool:
        # pylint: disable=unused-argument
        return self._check_permissions(self.read_permissions, user=user, raise_exception=False)

    # ---------------------------------------------------------------------------------------------------------------- #

    def rs_get(self, **data):
        self._check_permissions(self.read_permissions)
        x = self.get(self._get_id(data))
        return self.transform(x) if x is not None else None

    # ---------------------------------------------------------------------------------------------------------------- #

    def rs_list(self, **kw):
        self._check_permissions(self.read_permissions)

        offset = int(kw.get('start', 0))
        limit = int(kw.get('count', 50))
        filters = kw.get('filter') or {}
        # TODO: sorting

        data = [self.transform(x) for x in self.list(limit, offset, filters)]

        total_count = self.count(filters) # pylint: disable=assignment-from-none
        if total_count is None:
            total_count = len(data)

        return {
            'pos': offset,
            'total_count': total_count,
            'data': data
        }

    # ---------------------------------------------------------------------------------------------------------------- #

    def rs_insert(self, **data):
        self._check_permissions(self.write_permissions)
        x = self.insert(self.validate_data(None, data))
        return self.transform(x) if x is not None else None

    # ---------------------------------------------------------------------------------------------------------------- #

    def rs_update(self, **data):
        self._check_permissions(self.write_permissions)
        id = self._get_id(data)
        x = self.update(id, self.validate_data(id, data))
        return self.transform(x) if x is not None else None

    # ---------------------------------------------------------------------------------------------------------------- #

    def rs_delete(self, **data):
        self._check_permissions(self.delete_permissions)
        return self.delete(self._get_id(data))

    # ---------------------------------------------------------------------------------------------------------------- #

    def _check_permissions(self, permissions: str, *, user: Optional[User]=None, raise_exception: bool=True) -> bool:

        if permissions == 'everyone':
            return True

        if user is None:
            user = user_var.get()

        if user.has_permissions(permissions) is True:
            return True

        if raise_exception:
            raise Exception('permission denied')

        return False

    # ---------------------------------------------------------------------------------------------------------------- #

    def _get_id(self, data: dict) -> int:
        try:
            return int(data.get('id'))
        except:
            raise Exception('invalid/missing id')

# -------------------------------------------------------------------------------------------------------------------- #

class DbObjModel(BaseModel):

    dbobj: db.DbObj
    what: List[str] = ['*']
    data_fields: List[str] = ['data']


    def get(self, id: int) -> Any:
        return self.dbobj.get_by_id(id, what=','.join(self.what))


    def list(self, limit: Optional[int], offset: Optional[int], filters: dict) -> Any:
        # TODO: implement sorting
        where, vars = self.process_filters(filters)
        return self.dbobj.iter(what=','.join(self.what), where=where, vars=vars, limit=limit, offset=offset)


    def count(self, filters: dict) -> Optional[int]:
        where, vars = self.process_filters(filters)
        return db.query(f'SELECT COUNT(*) FROM {self.dbobj._table_name} WHERE {where}', **vars).fetchone()[0]


    def process_filters(self, filters: dict) -> Tuple[str, dict]:
        # pylint: disable=unused-argument
        return '1=1', {}


    def insert(self, data: dict) -> Any:
        return self.dbobj.insert(**data)


    def update(self, id: int, data: dict) -> Any:
        return db.query(f'''\
            UPDATE {self.dbobj._table_name} SET
            {', '.join(f'{k} = %({k})s' for k in data if k in self.dbobj._columns)}
            WHERE {self.dbobj._id_column} = {id:d}
            RETURNING {','.join(self.what)}
        ''', **{k: self.dbobj._encode(k, v) for k, v in data.items() if k in self.dbobj._columns}).fetchone()


    def delete(self, id: int) -> bool:
        r = db.query(f'DELETE FROM {self.dbobj._table_name} WHERE {self.dbobj._id_column} = {id:d}')
        return bool(r.rowcount)


    def transform(self, x: Any) -> dict:
        if '*' in self.what:
            x = dict(x.__dict__ if isinstance(x, db.DbObj) else x)
        else:
            d = x.__dict__ if isinstance(x, db.DbObj) else dict(x)
            x = {k: v for k, v in d.items() if k in self.what}
        for field in self.data_fields:
            if field in x:
                x.update(x.pop(field))
        return x

# -------------------------------------------------------------------------------------------------------------------- #

def model(name_or_mod=None, table=None):
    ''' model decorator. '''

    if callable(name_or_mod):
        plugins.register('core.webd.model', name_or_mod.__name__, name_or_mod)
        plugins.register('core.webd.model_from_table', camel_to_snake(name_or_mod.__name__), name_or_mod.__name__)
        return name_or_mod

    def inner(mod):
        n = name_or_mod or mod.__name__
        t = table or camel_to_snake(n)
        plugins.register('core.webd.model', n, mod)
        plugins.register('core.webd.model_from_table', t, n)
        return mod

    return inner

# -------------------------------------------------------------------------------------------------------------------- #
