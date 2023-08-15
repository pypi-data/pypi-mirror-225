# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from collections import OrderedDict
from typing import Iterator
import importlib
import os

import yaml

# -------------------------------------------------------------------------------------------------------------------- #

class Unit:
    ''' ... '''

    def __init__(self, name: str):

        unit_mod = importlib.import_module(name)

        self.name = name
        self.dir = str(unit_mod.__path__[0])

        def load_manifest(fn: str):
            manifest = os.path.join(self.dir, fn)
            if os.path.isfile(manifest):
                with open(manifest) as f:
                    return yaml.safe_load(f)
            return None

        # TODO: remove app.yml before v1.0.0
        self._manifest = load_manifest('unit.yml') or load_manifest('app.yml') or {}

    # ---------------------------------------------------------------------------------------------------------------- #

    def get_attr(self, key, default=None):
        ''' get attribute from unit manifest. key can include dots to reference sub-dicts. '''

        m = self._manifest
        parts = key.split('.')

        for part in parts[:-1]:
            m = m.get(part)
            if not isinstance(m, dict):
                return default

        return m.get(parts[-1], default)

    # ---------------------------------------------------------------------------------------------------------------- #

    def init_tables(self):

        db_mod = self.import_module('db')
        callback = getattr(db_mod, 'init_tables', None) if db_mod is not None else None

        from . import db
        with db.transaction():
            db.init_tables(self.name, callback)

    # ---------------------------------------------------------------------------------------------------------------- #

    def import_module(self, module):
        module = f'{self.name}.{module}'
        try:
            return importlib.import_module(module)
        except ModuleNotFoundError as e:
            if e.name == module:
                return None
            raise

    # ---------------------------------------------------------------------------------------------------------------- #

    def __repr__(self):
        return f'Unit({self.name})'

# -------------------------------------------------------------------------------------------------------------------- #

def init_unit(name: str) -> Unit:

    # already initialized?
    if name in _units:
        return _units[name]

    # instantiate unit
    u = _units[name] = Unit(name)

    # init dependencies
    for d in u.get_attr('dependencies', []):
        init_unit(d)

    return u

# -------------------------------------------------------------------------------------------------------------------- #

def get_unit(unit: str = 'main') -> Unit | None:
    return _units.get(unit)

# -------------------------------------------------------------------------------------------------------------------- #

def list_units() -> Iterator[Unit]:
    return _units.values()

# -------------------------------------------------------------------------------------------------------------------- #

_units = OrderedDict()

# -------------------------------------------------------------------------------------------------------------------- #
