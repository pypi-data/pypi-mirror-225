#!/usr/bin/env python3

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
