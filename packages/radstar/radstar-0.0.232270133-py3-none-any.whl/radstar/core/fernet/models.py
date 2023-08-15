# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from typing import Optional

from core.webd.lib import DbObjModel, model

from . import db

# -------------------------------------------------------------------------------------------------------------------- #

@model('rs.Secret')
class Secret(DbObjModel):

    read_permissions = 'super_user'
    write_permissions = 'super_user'
    delete_permissions = 'super_user'

    dbobj = db.Secret
    what = ['id', 'key']


    def validate_data(self, id: Optional[int], data: dict) -> dict:
        d = {'key': data['key']}
        if value := data.get('value'):
            d['value'] = value
        elif id is None:
            raise KeyError('value')
        return d

# -------------------------------------------------------------------------------------------------------------------- #
