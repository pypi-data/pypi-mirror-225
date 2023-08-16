# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=dangerous-default-value,redefined-builtin,too-many-arguments

# -------------------------------------------------------------------------------------------------------------------- #

from .funcs import query

# -------------------------------------------------------------------------------------------------------------------- #

class DbObj:

    _id_column = 'id'
    _table_name = None
    _columns = []

    _encoders = {}
    _decoders = {}

    # ---------------------------------------------------------------------------------------------------------------- #

    def __init__(self, record):
        for c in record.keys():
            if c == 'update':
                raise ValueError(f'column name "{c}" hides class member')
            super().__setattr__(c, self._decode(c, record[c]))

    # ---------------------------------------------------------------------------------------------------------------- #

    def __setattr__(self, name, value):

        if name == self._id_column:
            raise ValueError('can not change value of the id column')

        if name in self._columns:
            self.update(**{name: value})

        super().__setattr__(name, value)

    # ---------------------------------------------------------------------------------------------------------------- #

    def __iter__(self):
        yield from self.__dict__.items()

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def _decode(cls, column, value):
        if column in cls._decoders:
            return cls._decoders[column](value)
        return value

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def _encode(cls, column, value):
        if column in cls._encoders:
            return cls._encoders[column](value)
        return value

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def get(cls, where, vars={}, *, what='*'):
        obj = query(f'SELECT {what} FROM {cls._table_name} WHERE {where}', **vars).fetchone()
        return cls(obj) if obj is not None else None

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def get_by_id(cls, id, *, what='*', required=False):
        o = cls.get(f'{cls._id_column} = %(id)s', {'id': id}, what=what)
        if required is True and o is None:
            raise Exception(f'invalid {cls.__name__} {id=}')
        return o

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def iter(cls, *, what='*', where=None, order_by=None, limit=None, offset=None, vars={}):

        q = [ f'SELECT {what} FROM {cls._table_name}' ]
        if where is not None:
            q.append(f'WHERE {where}')
        if order_by is not None:
            q.append(f'ORDER BY {order_by}')
        if limit is not None:
            q.append(f'LIMIT {limit}')
        if offset is not None:
            q.append(f'OFFSET {offset}')

        for obj in query(' '.join(q), **vars):
            yield cls(obj)

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def list(cls, *, what='*', where=None, order_by=None, limit=None, offset=None, vars={}):
        return list(cls.iter(what=what, where=where, order_by=order_by, limit=limit, offset=offset, vars=vars))

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def listdict(cls, *, what='*', where=None, order_by=None, limit=None, offset=None, vars={}):

        q = [ f'SELECT {what} FROM {cls._table_name}' ]
        if where is not None:
            q.append(f'WHERE {where}')
        if order_by is not None:
            q.append(f'ORDER BY {order_by}')
        if limit is not None:
            q.append(f'LIMIT {limit}')
        if offset is not None:
            q.append(f'OFFSET {offset}')

        return [ dict(x) for x in query(' '.join(q), **vars) ]

    # ---------------------------------------------------------------------------------------------------------------- #

    @classmethod
    def insert(cls, **kw):
        q = f'''\
            INSERT INTO {cls._table_name} (
                {', '.join(k for k in kw if k in cls._columns)}
            ) VALUES (
                {', '.join(f'%({k})s' for k in kw if k in cls._columns)}
            ) RETURNING *
        '''
        return cls(query(q, **{k: cls._encode(k, v) for k, v in kw.items()}).fetchone())

    # ---------------------------------------------------------------------------------------------------------------- #

    def update(self, **kw):

        q = f'''\
            UPDATE {self._table_name} SET
            {', '.join(f'{k} = %({k})s' for k in kw if k in self._columns)}
            WHERE {self._id_column} = %(id_)s
        '''
        query(q, id_=getattr(self, self._id_column),
                **{k: self._encode(k, v) for k, v in kw.items() if k in self._columns})

        self.__dict__.update(kw)

# -------------------------------------------------------------------------------------------------------------------- #
