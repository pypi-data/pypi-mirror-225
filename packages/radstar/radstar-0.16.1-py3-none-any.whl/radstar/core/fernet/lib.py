# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from typing import Any, Optional

from cryptography.fernet import Fernet
from rs import json
from rs.db import query
from rs.utils import getenv, panic

# -------------------------------------------------------------------------------------------------------------------- #

def get(key: str, default: Optional[str]=None, *, required: bool=False):
    value = query('SELECT value FROM rs.secret WHERE key = %(key)s', key=key).fetchone()
    if value is None:
        if required is True:
            raise Exception(f'required secret missing: {key}')
        return default
    return decrypt(value[0])

# -------------------------------------------------------------------------------------------------------------------- #

def set(key: str, value: str):
    # pylint: disable=redefined-builtin
    query('''\
        INSERT INTO rs.secret (key, value) VALUES (%(key)s, %(value)s)
        ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
    ''', key=key, value=encrypt(value))

# -------------------------------------------------------------------------------------------------------------------- #

def decrypt(value: str) -> str:
    return _get_fernet().decrypt(value.encode()).decode()

def encrypt(value: str) -> str:
    return _get_fernet().encrypt(value.encode()).decode()

# -------------------------------------------------------------------------------------------------------------------- #

def decrypt_json(blob: str) -> Any:
    return json.loads(decrypt(blob))

def encrypt_json(obj: Any) -> str:
    return encrypt(json.dumps(obj))

# -------------------------------------------------------------------------------------------------------------------- #

def _get_fernet():
    # pylint: disable=used-before-assignment

    global _fernet
    if _fernet is not None:
        return _fernet

    # TODO: remove FERNET_KEY before v1.0.0
    if (fernet_key := getenv('RS_FERNET_KEY') or getenv('FERNET_KEY')) is None:
        panic('no fernet key specified')

    _fernet = Fernet(fernet_key)
    return _fernet

_fernet = None

# -------------------------------------------------------------------------------------------------------------------- #
