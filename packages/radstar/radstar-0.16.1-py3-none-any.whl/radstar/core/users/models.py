# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=abstract-method

# -------------------------------------------------------------------------------------------------------------------- #

from typing import Optional

from core.webd.lib import DbObjModel, model

from . import db

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.User')
class User(DbObjModel):

    read_permissions = 'super_user'
    write_permissions = 'super_user'
    delete_permissions = 'super_user'

    dbobj = db.User
    what = ['id', 'uid', 'name', 'super_user']


    def validate_data(self, id: Optional[int], data: dict) -> dict:
        d = {
            'uid': data['uid'],
            'name': data['name'],
            'super_user': bool(data.get('super_user', False)),
        }
        if pw := data.get('password'):
            d['password'] = pw
        elif id is None:
            raise Exception('missing password')
        return d

# -------------------------------------------------------------------------------------------------------------------- #
