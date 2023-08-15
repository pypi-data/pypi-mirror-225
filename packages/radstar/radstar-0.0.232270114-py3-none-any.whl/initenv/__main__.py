# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os
import sys

# -------------------------------------------------------------------------------------------------------------------- #

def main():
    ''' Init radstar environment. '''

    # check that we're executing in a radstar environment
    for dir_name in ['/rs', '/rs/project']:
        if not os.path.isdir(dir_name):
            print(f'invalid environment ({dir_name} missing)')
            sys.exit(1)

    # XXX: remove before v1.0.0
    for link_name in ['core', 'jetapp', 'rs', 'scripts', 'templates']:
        if os.path.islink((link_path := os.path.join('/rs/radstar', link_name))):
            os.unlink(link_path)
    if os.path.isdir('/rs/radstar') and not os.path.islink('/rs/radstar'):
        os.rmdir('/rs/radstar')
    # XXX: remove before v1.0.0

    # remove existing /rs/radstar link
    if os.path.islink('/rs/radstar'):
        os.unlink('/rs/radstar')

    # create /rs/radstar link
    link_src = os.path.dirname(os.path.dirname(__file__))
    if os.path.isdir(os.path.join(link_src, 'radstar')):
        link_src += '/radstar'
    os.symlink(link_src, '/rs/radstar')

    # setup apps
    os.execvp('rs', ['rs', 'setup-apps'])

# -------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------------- #
