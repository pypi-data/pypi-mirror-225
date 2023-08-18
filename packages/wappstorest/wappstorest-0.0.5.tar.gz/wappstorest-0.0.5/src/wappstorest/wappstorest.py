# -*- coding: utf-8 -*-
"""The Wappsto Rest Python API module."""
from __future__ import annotations

import uuid
import logging

from typing import Literal
from typing import overload

from .wappsto_service_builder import WappstoServiceBuilder

from .wappsto_service_builder import WappstoSessionBuilder
from .wappsto_service_builder import WappstoUserBuilder
from .wappsto_service_builder import get_builder

from .schemas.base import WappstoEnv
from .schemas.base import WappstoService
from .schemas.base import WappstoVersion
from .schemas import WappstoSchema

from rich.console import Console

console = Console()

name = "WappstoRest"
__version__ = "v0.0.1"


class WappstoRest:
    """
    WappstoRest is a helper class for interacting with the Wappsto REST service.

    WappstoRest offers an Fluent interface to build up the request make to Wappsto.
    """

    def __init__(
        self,
        env: WappstoEnv = WappstoEnv.PROD,
        version: WappstoVersion = WappstoVersion.V2_1,
        session: uuid.UUID | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        """
        Initialization of the Wappsto REST connection.

        Args:
            env: The Wappsto Environment to connect to. (Default: PROD)
            session: (Optional) If a user session created to be used.
            username: (Optional) The Wappsto Login, to create a user session.
            password: (Optional) Password for the Wappsto Login.
        """
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

        self.vr: WappstoVersion = version
        self.env: WappstoEnv = env
        self.admin_session: uuid.UUID | None = None
        self.default_session: uuid.UUID | None = None

        self.base_url = "wappsto.com"
        self.service_url = f"{self.base_url}/services"
        self.__set_wappsto_enviroment(env=env)
        if session:
            self.set_session(session=session)

    def __set_wappsto_enviroment(self, env: WappstoEnv):
        self.base_url = f"{env.value + '.' if env != WappstoEnv.PROD else ''}wappsto.com"
        self.service_url = f"{self.base_url}/services"

    def set_session(self, session: uuid.UUID, admin: bool = False):
        """
        Set a premake session UUID.

        Args:
            session: The Session UUID to be set.
            admin: If True, the session UUID given will be
                   save as a admin session.
        """
        if admin is True:
            self.admin_session = session
        else:
            self.default_session = session

    def login(self, username: str, password: str, admin: bool = False) -> bool:
        """
        Login and create a session for given user.

        # TODO: Add handle of admin.

        Args:
            username: The Wappsto Login.
            password: Password for the Wappsto Login.
            admin: If True, login as a admin.

        Returns:
            True, if the task was successful else
            False.
        """
        data: WappstoSchema.Create.Session = WappstoSchema.Create.Session(
            username=username,
            password=password,
            remember_me=False
        )

        session = self.service(WappstoService.SESSION)

        if admin is True:
            session = session.admin()

        new_session = session.create(
            data=data
        )

        self.default_session = new_session.meta.id

        return True

    def logout(self, admin: bool = False) -> bool:
        """
        Logout of the session.

        # TODO: Add handle of admin.

        Args:
            admin: IF True, logout the admin session.

        Returns:
            True, if the task was successful else
            False.
        """
        if self.default_session is None:
            return False

        self.service(WappstoService.SESSION).service_id(
            self.default_session,
        ).delete()

        self.default_session = None

        return True

    @overload
    def service(
        self,
        wappsto_service: Literal[WappstoService.SESSION.value]
    ) -> WappstoSessionBuilder: ...

    @overload
    def service(
        self,
        wappsto_service: Literal[WappstoService.USER.value]
    ) -> WappstoUserBuilder: ...

    def service(self, wappsto_service: WappstoService) -> WappstoServiceBuilder:
        """
        Start building an service request.

        Args:
            wappsto_service: The Wappsto Service that should connect to.

        Returns:
            Reference to self.
        """
        return get_builder.get(wappsto_service, WappstoServiceBuilder)(
            wappsto_service=wappsto_service,
            rest_ref=self
        )
