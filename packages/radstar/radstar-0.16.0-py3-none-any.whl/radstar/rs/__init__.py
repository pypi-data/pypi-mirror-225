# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from rsrpc import json

from . import db, plugins, settings, unit
from .plugins import plugin

from .unit import get_unit, list_units
from .utils import attrs, camel_to_snake, getenv, panic, readfile, shsplit

# -------------------------------------------------------------------------------------------------------------------- #

def init(modules: list[str] | None = None, *, import_default_modules: bool = True) -> unit.Unit | None:
    ''' init function. can be called multiple times. '''

    if get_unit('main') is None:
        unit.init_unit('core.core')
        unit.init_unit('main')

    def import_modules_in_all_units(modules: list[str]):
        for u in list_units():
            for m in modules:
                u.import_module(m)

    # import default modules
    if import_default_modules is True and not _default_modules_imported:
        import_modules_in_all_units(['lib', 'app'])
        _default_modules_imported.append(True)

    # import requested modules
    if modules is not None:
        import_modules_in_all_units(modules)

    return get_unit('main')

# -------------------------------------------------------------------------------------------------------------------- #

_default_modules_imported = []

# -------------------------------------------------------------------------------------------------------------------- #
