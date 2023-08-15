# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os

import tempfile

from . import cli

# -------------------------------------------------------------------------------------------------------------------- #

INIT_CODE = '''\
import rs
main = rs.init()
db = main.import_module('db')
'''

# -------------------------------------------------------------------------------------------------------------------- #

@cli.command()
def python():
    ''' Launch python interpreter with radstar initialized. '''

    with tempfile.TemporaryDirectory() as td:
        startup = os.path.join(td, 'startup.py')

        with open(startup, 'w') as f:
            f.write(INIT_CODE)

        os.system(f"PYTHONSTARTUP='{startup}' python3")

# -------------------------------------------------------------------------------------------------------------------- #
