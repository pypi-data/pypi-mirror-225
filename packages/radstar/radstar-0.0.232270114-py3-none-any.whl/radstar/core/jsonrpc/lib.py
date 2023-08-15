# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from rs import plugins

PLUGIN_KEY = 'core.jsonrpc.method'

# -------------------------------------------------------------------------------------------------------------------- #

def rpc_method(name_or_func=None):

    if callable(name_or_func):
        plugins.register(PLUGIN_KEY, name_or_func.__name__, name_or_func)
        return name_or_func

    def inner(func):
        plugins.register(PLUGIN_KEY, name_or_func or func.__name__, func)
        return func

    return inner

# -------------------------------------------------------------------------------------------------------------------- #

class RPCError(Exception):
    def __init__(self, code, msg):
        # pylint: disable=super-init-not-called
        self.code = code
        self.msg = msg

# -------------------------------------------------------------------------------------------------------------------- #
