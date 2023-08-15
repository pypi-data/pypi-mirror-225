# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=redefined-builtin

# -------------------------------------------------------------------------------------------------------------------- #

from collections import defaultdict

# -------------------------------------------------------------------------------------------------------------------- #

_plugins_by_type = defaultdict(dict)
_plugins_by_label = defaultdict(dict)

# -------------------------------------------------------------------------------------------------------------------- #

def plugin(type, name=None, *, labels=[]):
    def inner(p):
        register(type, name or p.__name__, p, labels=labels)
        return p
    return inner

# -------------------------------------------------------------------------------------------------------------------- #

def register(type, name, p, *, labels=[]):
    # pylint: disable=dangerous-default-value
    _plugins_by_type[type][name] = p
    for l in labels:
        _plugins_by_label[l][name] = p

# -------------------------------------------------------------------------------------------------------------------- #

def get(type, name, default=None):
    return _plugins_by_type[type].get(name, default)

# -------------------------------------------------------------------------------------------------------------------- #

def list(*, type=None, label=None):
    match (type, label):
        case type, None:
            return _plugins_by_type[type].items()
        case None, label:
            return _plugins_by_label[label].items()
        case type, label:
            return [x for x in _plugins_by_type[type].items() if x[0] in _plugins_by_label[label]]
    return []

# -------------------------------------------------------------------------------------------------------------------- #
