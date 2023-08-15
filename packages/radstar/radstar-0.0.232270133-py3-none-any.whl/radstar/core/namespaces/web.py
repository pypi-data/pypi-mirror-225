# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import bcrypt

from core.webd.lib import User
from rs import db, plugin

from .db import Namespace

# -------------------------------------------------------------------------------------------------------------------- #

class NamespaceUser(User):

    def __init__(self, id: int, super_user: bool):
        self.id = id
        self.super_user = super_user
        self.ns_id = 0
        self.ns_admin = False

    def has_permissions(self, permissions: str) -> bool:

        if permissions == 'user':
            return True

        if permissions == 'ns_admin' and self.ns_admin is True:
            return True

        if permissions == 'super_user' and self.super_user is True:
            return True

        return False

# -------------------------------------------------------------------------------------------------------------------- #

@plugin('core.webd', 'auth')
class NamespaceAuth:

    @staticmethod
    def authenticate(username, password):

        # get user namespace from database
        with db.transaction():
            user = Namespace.get(where='uid = %(uid)s', vars={'uid': username})
            if user is None or not user.password:
                return None

        # check that password matches
        if bcrypt.checkpw(password.encode(), bytes(user.password)) is not True:
            return None

        return NamespaceUser(user.id, user.super_user)

    # ---------------------------------------------------------------------------------------------------------------- #

    @staticmethod
    def welcome(user, hello_data):
        assert isinstance(user, NamespaceUser)

        ns_id = int(hello_data.get('ns_id', 0))

        if ns_id in (0, user.id):
            # personal namespace requested
            ns_id, admin = user.id, True

        else:
            # different namespace requested

            if user.super_user is True:
                query = 'SELECT TRUE FROM rs.namespace WHERE id = %(ns_id)s'
            else:
                query = 'SELECT admin FROM rs.member WHERE namespace_id = %(ns_id)s AND member_id = %(user_id)s'

            with db.transaction():
                if (res := db.query(query, ns_id=ns_id, user_id=user.id).fetchone()) is not None:
                    # namespace found and we have access
                    admin = res[0]
                else:
                    # namespace not found or no access, connect to personal namespace
                    ns_id, admin = user.id, True

        # update user object
        user.ns_id = ns_id
        user.ns_admin = admin

        # data to be sent to the client
        return {
            'ns_id': ns_id,
            'admin': admin,
            'super_user': user.super_user,
        }

# -------------------------------------------------------------------------------------------------------------------- #
