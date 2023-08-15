#!/usr/bin/env python3

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

import sys

while True:

    # transition from ACKNOWLEDGED to READY
    sys.stdout.write('READY\n')

    # read headers
    line = sys.stdin.readline().strip()
    headers = dict([x.split(':') for x in line.split()])

    # read event payload
    data = sys.stdin.read(int(headers['len']))
    event, data = data.split('\n', 1)
    event = dict([x.split(':') for x in event.split()])
    process = event['processname']

    # write log to stderr
    for line in data.splitlines():
        print(f'[{process}] {line.strip()}', file=sys.stderr)

    # transition from READY to ACKNOWLEDGED
    sys.stdout.write('RESULT 2\nOK')
