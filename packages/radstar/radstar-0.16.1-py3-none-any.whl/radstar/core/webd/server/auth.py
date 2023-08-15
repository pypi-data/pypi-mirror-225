# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# pylint: disable=unused-argument

# -------------------------------------------------------------------------------------------------------------------- #

import asyncio
from contextvars import ContextVar
from typing import Optional

from rs import plugins
import aiohttp

from . import routes

# -------------------------------------------------------------------------------------------------------------------- #

class User:

    def has_permissions(self, permissions: str) -> bool:
        ''' check if the user has the requested permissions. '''
        return False


user_var: ContextVar[Optional[User]] = ContextVar('user')

# -------------------------------------------------------------------------------------------------------------------- #

class Auth:

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        ''' authenticate user using username and password. '''
        return None

    @staticmethod
    def welcome(user: User, hello_data: dict) -> Optional[dict]:
        ''' called on websocket welcome. '''
        return None


def get_auth_plugin() -> Auth:
    return plugins.get('core.webd', 'auth', Auth)

# -------------------------------------------------------------------------------------------------------------------- #

@routes.get('/_auth')
async def auth_handler(request):

    def fail():
        raise aiohttp.web.HTTPUnauthorized(headers={'WWW-Authenticate': f'Basic realm="{rs.get_unit().name}"'})

    def authenticate_user():
        ap = get_auth_plugin()

        # get and parse authorization header
        try:
            auth = aiohttp.BasicAuth.decode(auth_header=request.headers.getone(aiohttp.hdrs.AUTHORIZATION))
        except:
            fail()

        # authenticate user
        user = ap.authenticate(auth.login, auth.password)
        if user is None:
            fail()

        # check that the user has super user permissions
        if user.has_permissions('super_user') is not True:
            fail()

    await asyncio.to_thread(authenticate_user)
    return aiohttp.web.Response(text='ok')

# -------------------------------------------------------------------------------------------------------------------- #
