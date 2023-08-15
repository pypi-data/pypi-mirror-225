# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import bcrypt

from core.webd.lib import auth
import rs

from . import db

# -------------------------------------------------------------------------------------------------------------------- #

class User(auth.User):

    def __init__(self, id: int, super_user: bool):
        self.id = id
        self.super_user = super_user


    def has_permissions(self, permissions: str) -> bool:

        if permissions == 'user':
            return True

        if permissions == 'super_user' and self.super_user is True:
            return True

        return False

# -------------------------------------------------------------------------------------------------------------------- #

@rs.plugin('core.webd', 'auth')
class NamespaceAuth:

    @staticmethod
    def authenticate(username, password):

        # get user from database
        with rs.db.transaction():
            user = db.User.get(where='uid = %(uid)s', vars={'uid': username})
            if user is None or not user.password:
                return None

        # check that password matches
        if bcrypt.checkpw(password.encode(), bytes(user.password)) is not True:
            return None

        return User(user.id, user.super_user)

    # ---------------------------------------------------------------------------------------------------------------- #

    @staticmethod
    def welcome(user, hello_data):
        # pylint: disable=unused-argument

        assert isinstance(user, User)

        # data to be sent to the client
        return {
            'super_user': user.super_user,
        }

# -------------------------------------------------------------------------------------------------------------------- #
