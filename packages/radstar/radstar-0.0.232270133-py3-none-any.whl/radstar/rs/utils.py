# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import logging
import os
import shlex
import sys

# -------------------------------------------------------------------------------------------------------------------- #

def attrs(**kw):
    ''' decorator for setting attributes on a function. '''

    def inner(func):
        for k, v in kw.items():
            setattr(func, k, v)
        return func

    return inner

# -------------------------------------------------------------------------------------------------------------------- #

def camel_to_snake(name):

    rv = ''
    in_upper = False

    for x in name:
        if x.isupper():
            if rv and rv[-1].isalnum() and not in_upper:
                rv += '_'
            rv += x.lower()
            in_upper = True
        else:
            rv += x
            in_upper = False

    return rv

# -------------------------------------------------------------------------------------------------------------------- #

def getenv(var, default=None, *, convert=str):
    if (file_name := os.getenv(var + '_FILE')) is not None:
        return readfile(file_name, default, convert=convert)
    if (value := os.getenv(var)) is not None:
        return convert(value)
    return default

# -------------------------------------------------------------------------------------------------------------------- #

def panic(msg, *, exc_info=False):
    logging.critical(msg, exc_info=exc_info)
    sys.exit(1)

# -------------------------------------------------------------------------------------------------------------------- #

def readfile(fn, default=None, *, convert=str):
    ''' read value from first line of named file. '''
    try:
        with open(fn) as f:
            return convert(f.readline().strip())
    except IOError:
        return default

# -------------------------------------------------------------------------------------------------------------------- #

def shsplit(cmd_: str, **kw):
    ''' split shell command to array. '''
    return [x.format(**kw) for x in shlex.split(cmd_)]

# -------------------------------------------------------------------------------------------------------------------- #
