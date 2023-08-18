import uuid
import logging
import json
import pathlib

from io import IOBase

import httpx
import pydantic

from .core.exceptions import WappstoError

from .schemas.base import WappstoService
from .schemas import WappstoSchema

from rich.console import Console

console = Console()


class WappstoServiceBuilder:
    """
    Wappsto Service Builder, is a constructor class to build out the request.

    Wappsto Service Builder is a parent class, to be inherited from, for all
    the service, there is, where the only changes are a overload of the
    'Execution' methods, to set the right return types for each one.

    NOTE: https://mail.python.org/pipermail/python-dev/2003-October/038855.html
    """

    def __init__(self, wappsto_service: WappstoService, rest_ref: 'WappstoRest'):
        """
        Initialization of the Wappsto Service constructor.

        Args:
            wappsto_service: The Wappsto Service that should connect to.
            rest_ref: Ref to the Base Rest class.
        """
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

        self._admin: bool = False
        self._file: pathlib.Path | IOBase | None = None
        self._filters: list[str] = []
        self._headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        self._options: dict[str, str | int | float] = {}
        self._parent: dict[uuid.UUID, WappstoService] = {}
        self._service_id: uuid.UUID | None = None
        self.rest_ref: 'WappstoRest' = rest_ref
        self._service: WappstoService = wappsto_service

        self._set_session_to_default()

    def _build_url(
        self,
        service_uuid: uuid.UUID | None = None,
        subservice: WappstoService | None = None,
    ) -> str:
        _vr = self.rest_ref.vr
        url = self.rest_ref.service_url
        service_path: str = "/"
        _parent_id, _parent_service = list(self._parent.items())[0] if self._parent else (None, None)
        if _parent_id:
            service_path += f"{_parent_service.value}/{str(_parent_id)}/"

        service_path += f"{self._service.value}"

        if self._service_id:
            service_path += f"/{str(self._service_id)}"

        if not self._admin:
            return f"https://{url}/{_vr.value}{service_path}"
        return f"https://admin.{url}/{_vr.value}{service_path}"

    def _build_filters(self) -> str:
        the_great_filter: str = "&".join(
            map(lambda x: str(x), self._filters)
        )
        return "" if not the_great_filter else "?" + the_great_filter

    def _set_session_to_default(self):
        if self.rest_ref.default_session is not None:
            self._headers["x-session"] = str(self.rest_ref.default_session)

    def filter(self, filter: str) -> 'WappstoServiceBuilder':
        """
        Applying a filter the the service request.

        Args:
            filter: The filter Criteria to be applied.

        Returns:
            Reference to self.
        """
        self._filters.append(filter)
        return self

    def header(self, **kwargs: str | int | float) -> 'WappstoServiceBuilder':
        """
        Applying a header to the request.

        Args:
            **kwargs: The Header key and value pair.

        Returns:
            Reference to self.
        """
        self._headers.update({
            key: str(value) for key, value in kwargs.items()
        })
        return self

    def option(self, **kwargs: str | int | float) -> 'WappstoServiceBuilder':
        """
        Set a parameter on the request.

        Args:
            **kwargs: The Option key and value pair.

        Returns:
            Reference to self.
        """
        self._options.update(kwargs)
        return self

    def verbose(self) -> 'WappstoServiceBuilder':
        """
        Set the verbose parameter on the request.

        Returns:
            Reference to self.
        """
        self._options.update({'verbose': True})
        return self

    def admin(self) -> 'WappstoServiceBuilder':
        """
        Set the Request to be a admin based request.

        Returns:
            Reference to self.
        """
        self._admin = True
        if self.rest_ref.admin_session is not None:
            self._headers["x-session"] = str(self.rest_ref.admin_session)
        return self

    def parent(
        self,
        parent_id: uuid.UUID,
        parent_service: WappstoService,
    ) -> 'WappstoServiceBuilder':
        """
        Set the parent for the current Wappsto Service.

        Args:
            parent_id: The UUID of the parent.
            parent_service: The Service of the parent.

        Returns:
            Reference to self.
        """
        self._parent[parent_id] = parent_service
        return self

    def service_id(self, service_id: uuid.UUID) -> 'WappstoServiceBuilder':
        """
        Set the UUID of the current service.

        Args:
            service_id: The service UUID for the given service.

        Returns:
            Reference to self.
        """
        self._service_id = service_id
        return self

    def upload_file(self, file_obj: pathlib.Path | IOBase) -> 'WappstoServiceBuilder':
        """
        Set a File to be uploaded.

        Args:
            file_obj: The path to the file, or a file object.

        Returns:
            Reference to self.
        """
        self._file = file_obj
        return self

    """The Execution of the Request."""

    def _ready_data(self) -> str:
        """
        Ready all the data needed for a request.

        This function readies:
         - URL
         - Headers
         - Parameter
         - Options
         - Filters
        """
        the_url: str = self._build_url()
        the_url += self._build_filters()
        return the_url

    def _exception_builder(self, rdata: httpx.Response):
        """
        Check which level the problem came and raise the right Exception.

        Raise:
            WappstoError: Wappsto Problems.
            ConnectionError: Network Problems.
        """
        try:
            the_data = rdata.json()
        except json.JSONDecodeError:
            raise ConnectionError("An error happened doing request.")
        else:
            raise WappstoError(
                code=the_data.get('code'),
                msg=the_data.get('message'),
                url=str(rdata.url),
                http_code=rdata.status_code
            )

    def read(self, expand: int | None = None) -> dict:
        """
        Building and sending the HTTP GET request.

        Args:
            expand: (Optional) If the data returned should be expanded.

        Raise:
            WappstoError: Wappsto Problems.
            ConnectionError: Network Problems.
            httpx.HTTPError  (TODO: FIXME!)
        """
        options = {**self._options}
        if expand is not None:
            options['expand'] = expand
        url: str = self._ready_data()
        rdata = httpx.get(
            url=url,
            headers=self._headers,
            params=options,
        )

        full_url = rdata.url

        if rdata.status_code >= 300:
            console.log(f"service:{self._service.value} -> get", log_locals=True)
            self._exception_builder(rdata)

        r_data = rdata.json()

        if logging.root.level <= logging.INFO:
            console.log(f"service:{self._service.value} -> get", log_locals=True)

        return r_data

    def delete(self) -> dict:
        """
        Building and sending the HTTP DELETE request.

        Raise:
            WappstoError: Wappsto Problems.
            ConnectionError: Network Problems.
            httpx.HTTPError  (TODO: FIXME!)
        """
        url: str = self._ready_data()
        rdata = httpx.delete(
            url=url,
            headers=self._headers,
            params=self._options,
        )

        full_url = rdata.url

        if rdata.status_code >= 300:
            console.log(f"service:{self._service.value} -> delete", log_locals=True)
            self._exception_builder(rdata)

        r_data = rdata.json()

        if logging.root.level <= logging.INFO:
            console.log(f"service:{self._service.value} -> delete", log_locals=True)

        return r_data

    def create(self, data: dict | str) -> dict:
        """
        Building and sending the HTTP POST request.

        Args:
            data: The data object to be created.

        Raise:
            WappstoError: Wappsto Problems.
            ConnectionError: Network Problems.
            httpx.HTTPError  (TODO: FIXME!)
        """
        print(self._headers)
        url: str = self._ready_data()
        rdata = httpx.post(
            url=url,
            headers=self._headers,
            params=self._options,
            json=data if isinstance(data, dict) else None,
            content=data.encode() if isinstance(data, str) else None,
        )

        full_url = rdata.url

        if rdata.status_code >= 300:
            console.log(f"service:{self._service.value} -> create", log_locals=True)
            self._exception_builder(rdata)

        r_data = rdata.json()

        if logging.root.level <= logging.INFO:
            console.log(f"service:{self._service.value} -> create", log_locals=True)

        return r_data

    def update(self, data: dict | str, overwrite: bool = False) -> dict:
        """
        Building and sending the HTTP PUT request.

        Args:
            data: The data object to be updated with.

        Raise:
            WappstoError: Wappsto Problems.
            ConnectionError: Network Problems.
            httpx.HTTPError  (TODO: FIXME!)
        """
        url: str = self._ready_data()

        httpxupdate = httpx.patch if overwrite is True else httpx.put

        rdata = httpxupdate(
            url=url,
            headers=self._headers,
            params=self._options,
            json=data if isinstance(data, dict) else None,
            content=data.encode() if isinstance(data, str) else None,
        )

        full_url = rdata.url

        if rdata.status_code >= 300:
            console.log(f"service:{self._service.value} -> update", log_locals=True)
            self._exception_builder(rdata)

        r_data = rdata.json()

        if logging.root.level <= logging.INFO:
            console.log(f"service:{self._service.value} -> update", log_locals=True)

        return r_data


class WappstoSessionBuilder(WappstoServiceBuilder):
    def read(
        self, expand: int | None = None
    ) -> WappstoSchema.response.Session | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Session]:
        r_data = super().read(expand=expand)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Session | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Session],
            r_data
        )

    def delete(self) -> WappstoSchema.response.Session | WappstoSchema.response.DeleteList:
        r_data = super().delete()
        return pydantic.parse_obj_as(
            WappstoSchema.response.Session | WappstoSchema.response.DeleteList,
            r_data
        )
    def create(self, data: WappstoSchema.create.Session) -> WappstoSchema.response.Session | list[WappstoSchema.response.Session]:
        r_data = super().create(data=data.json(exclude_none=True))
        return pydantic.parse_obj_as(
            WappstoSchema.response.Session | list[WappstoSchema.response.Session],
            r_data
        )
    def update(self, data: WappstoSchema.update.Session, overwrite: bool = False) -> WappstoSchema.response.Session:
        r_data = super().update(data=data.json(exclude_none=True), overwrite=overwrite)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Session,
            r_data
        )


class WappstoUserBuilder(WappstoServiceBuilder):
    def read(
        self, expand: int | None = None
    ) -> WappstoSchema.response.User | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.User]:
        r_data = super().read(expand=expand)
        return pydantic.parse_obj_as(
            WappstoSchema.response.User | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.User],
            r_data
        )

    def delete(self) -> WappstoSchema.response.User | WappstoSchema.response.DeleteList:
        r_data = super().delete()
        return pydantic.parse_obj_as(
            WappstoSchema.response.User | WappstoSchema.response.DeleteList,
            r_data
        )
    def create(self, data: WappstoSchema.create.User) -> WappstoSchema.response.User | list[WappstoSchema.response.User]:
        r_data = super().create(data=data.json(exclude_none=True))
        return pydantic.parse_obj_as(
            WappstoSchema.response.User | list[WappstoSchema.response.User],
            r_data
        )
    def update(self, data: WappstoSchema.update.User, overwrite: bool = False) -> WappstoSchema.response.User:
        r_data = super().update(data=data.json(exclude_none=True), overwrite=overwrite)
        return pydantic.parse_obj_as(
            WappstoSchema.response.User,
            r_data
        )


class WappstoNetworkBuilder(WappstoServiceBuilder):
    def read(
        self, expand: int | None = None
    ) -> WappstoSchema.response.Network | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Network]:
        r_data = super().read(expand=expand)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Network | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Network],
            r_data
        )

    def delete(self) -> WappstoSchema.response.Network | WappstoSchema.response.DeleteList:
        r_data = super().delete()
        return pydantic.parse_obj_as(
            WappstoSchema.response.Network | WappstoSchema.response.DeleteList,
            r_data
        )
    def create(self, data: WappstoSchema.create.Network) -> WappstoSchema.response.Network | list[WappstoSchema.response.Network]:
        r_data = super().create(data=data.json(exclude_none=True))
        return pydantic.parse_obj_as(
            WappstoSchema.response.Network | list[WappstoSchema.response.Network],
            r_data
        )
    def update(self, data: WappstoSchema.update.Network, overwrite: bool = False) -> WappstoSchema.response.Network:
        r_data = super().update(data=data.json(exclude_none=True), overwrite=overwrite)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Network,
            r_data
        )


class WappstoDeviceBuilder(WappstoServiceBuilder):
    def read(
        self, expand: int | None = None
    ) -> WappstoSchema.response.Device | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Device]:
        r_data = super().read(expand=expand)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Device | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Device],
            r_data
        )

    def delete(self) -> WappstoSchema.response.Device | WappstoSchema.response.DeleteList:
        r_data = super().delete()
        return pydantic.parse_obj_as(
            WappstoSchema.response.Device | WappstoSchema.response.DeleteList,
            r_data
        )
    def create(self, data: WappstoSchema.create.Device) -> WappstoSchema.response.Device | list[WappstoSchema.response.Device]:
        r_data = super().create(data=data.json(exclude_none=True))
        return pydantic.parse_obj_as(
            WappstoSchema.response.Device | list[WappstoSchema.response.Device],
            r_data
        )
    def update(self, data: WappstoSchema.update.Device, overwrite: bool = False) -> WappstoSchema.response.Device:
        r_data = super().update(data=data.json(exclude_none=True), overwrite=overwrite)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Device,
            r_data
        )


class WappstoValueBuilder(WappstoServiceBuilder):
    def read(
        self, expand: int | None = None
    ) -> WappstoSchema.response.Value | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Value]:
        r_data = super().read(expand=expand)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Value | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.Value],
            r_data
        )

    def delete(self) -> WappstoSchema.response.Value | WappstoSchema.response.DeleteList:
        r_data = super().delete()
        return pydantic.parse_obj_as(
            WappstoSchema.response.Value | WappstoSchema.response.DeleteList,
            r_data
        )
    def create(self, data: WappstoSchema.create.Value) -> WappstoSchema.response.Value | list[WappstoSchema.response.Value]:
        r_data = super().create(data=data.json(exclude_none=True))
        return pydantic.parse_obj_as(
            WappstoSchema.response.Value | list[WappstoSchema.response.Value],
            r_data
        )
    def update(self, data: WappstoSchema.update.Value, overwrite: bool = False) -> WappstoSchema.response.Value:
        r_data = super().update(data=data.json(exclude_none=True), overwrite=overwrite)
        return pydantic.parse_obj_as(
            WappstoSchema.response.Value,
            r_data
        )


class WappstoStateBuilder(WappstoServiceBuilder):
    def read(
        self, expand: int | None = None
    ) -> WappstoSchema.response.State | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.State]:
        r_data = super().read(expand=expand)
        return pydantic.parse_obj_as(
            WappstoSchema.response.State | WappstoSchema.response.IdList | WappstoSchema.response.AttributeList | list[WappstoSchema.response.State],
            r_data
        )

    def delete(self) -> WappstoSchema.response.State | WappstoSchema.response.DeleteList:
        r_data = super().delete()
        return pydantic.parse_obj_as(
            WappstoSchema.response.State | WappstoSchema.response.DeleteList,
            r_data
        )
    def create(self, data: WappstoSchema.create.State) -> WappstoSchema.response.State | list[WappstoSchema.response.State]:
        r_data = super().create(data=data.json(exclude_none=True))
        return pydantic.parse_obj_as(
            WappstoSchema.response.State | list[WappstoSchema.response.State],
            r_data
        )
    def update(self, data: WappstoSchema.update.State, overwrite: bool = False) -> WappstoSchema.response.State:
        r_data = super().update(data=data.json(exclude_none=True), overwrite=overwrite)
        return pydantic.parse_obj_as(
            WappstoSchema.response.State,
            r_data
        )


# class WappstoUserBuilder(WappstoServiceBuilder):
#     def read(
#         self, expand: int | None = None
#     ) -> WappstoSchema.User: ...
#     def delete(self) -> WappstoSchema.User: ...
#     def create(self, data: WappstoSchema.User) -> WappstoSchema.User: ...
#     def update(self, data: WappstoSchema.User) -> WappstoSchema.User: ...


get_builder = {
    WappstoService.USER: WappstoUserBuilder,
    WappstoService.SESSION: WappstoSessionBuilder,
    WappstoService.NETWORK: WappstoNetworkBuilder,
    WappstoService.DEVICE: WappstoDeviceBuilder,
    WappstoService.VALUE: WappstoValueBuilder,
    WappstoService.STATE: WappstoStateBuilder,
}
