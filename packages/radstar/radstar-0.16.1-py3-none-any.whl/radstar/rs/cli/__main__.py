# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=unexpected-keyword-arg,unused-import

import os

# -------------------------------------------------------------------------------------------------------------------- #

def main():

    from . import (
        cli,

        configure,
        db,
        deps,
        python,
        run,
        setup,
    )

    home_dir = __file__
    for _ in range(3):
        home_dir = os.path.dirname(home_dir)
    os.chdir(home_dir)

    cli(prog_name='rs')

# -------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------------- #
