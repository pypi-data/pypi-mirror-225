#!/usr/bin/env python3

import os
import re

FIND = re.compile(r'''\
(#|\/\/) Copyright .*?
(#|\/\/) SPDX-License-Identifier: .*?
''')

REPLACE = '''
{comment} Copyright © 2021-2023 Peter Mathiasson
{comment} SPDX-License-Identifier: ISC
'''

for root, dirs, files in os.walk('.'):

    for fn in files:

        if fn == 'update-copyright.py':
            continue

        ext = os.path.splitext(fn)[1]
        fn = os.path.join(root, fn)

        if ext in ['.py', '.sh']:
            comment = '#'
        elif ext in ['.js']:
            comment = '//'
        else:
            continue

        with open(fn) as f:
            data = f.read()

        new_data = FIND.sub(REPLACE.format(comment=comment), data)

        if new_data != data:
            print('updating', fn)

            with open(fn, 'w') as f:
                f.write(new_data)

print('done. do not forget to update LICENSE file.')
