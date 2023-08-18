#!/usr/bin/env python

###############################################################################
#
# Wappsto Websocket
#
# Wappsto Websocket is used to get live change update.
#
#
#
# Link:
# https://documentation.dev.wappsto.com/#/docs/streaming/streaming
#
###############################################################################

import json
import logging
import httpx
import threading
import urllib
import uuid

from pydantic import parse_obj_as
from pydantic import ValidationError

from typing import Any
from typing import Callable
from typing import Dict
from typing import Union

# TODO: Use SlxJsonRpc for the Configuration messages. Instead of:

import websocket

from .schemas.base import WappstoService
from .schemas.websocket_schema import EventStreamSchema
from .schemas.websocket_schema import RPCRequest
from .schemas.websocket_schema import RPCSuccess
from .schemas.websocket_schema import HttpMethods 


name = "WappstoWS"
__version__ = "v0.5.0"


class WappstoWebSocket:
    def __init__(
        self,
        session=None,
        username=None,
        password=None,
        service="wappsto.com",
        parameters=None,
        full=True,
        version="2.1",
        timeout=None,
    ):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())
        # websocket.enableTrace(True)

        self.version = version
        self.url = f"{service}/services/{self.version}"
        self.parameters: dict

        self.open = False
        self.timeout = timeout

        if not session:
            if not username or not password:
                msg = "missing required positional argument(s): "
                msg += "'username' " if not username else ""
                msg += "'password' " if not password else ""
                raise TypeError(msg)
            session = self._create_session(username=username, password=password)
            if not session:
                msg = "An Error happened doing session creation."
                self.log.error(msg)
                raise ConnectionError(msg)

        if not isinstance(parameters, dict):
            self.parameters: dict = {}
        else:
            self.parameters = parameters

        self.parameters["X-session"] = session
        self.parameters["full"] = full

        # self.parameters['subscription'] = "[" + ",".join(sub_type) + "]"
        # websocket.enableTrace(True)

        # To keep track of the config msg.
        self._config_reply_wait: Dict[str, Any] = {}

        self.callback_list: Dict[
            uuid.UUID, Callable[[uuid.UUID, EventStreamSchema], None]
        ] = {}

        # self._unused_data = []

        self.ws = websocket.WebSocketApp(
            url=self._get_ws_link(),
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_open=self.__on_open,
            # on_ping= self.__on_ping,
            # on_pong=self.__on_pong,
            # on_count=self.__on_count,
            on_close=self.__on_close,
        )
        self.wst = threading.Thread(target=self.ws.run_forever)
        # self.wst.daemon = True
        self.wst.start()

    def is_open(self):
        return self.open

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _config_wait(self, _id: str, data):
        """Send the config data, & wait for reply."""
        _temp_event = threading.Event()
        self._config_reply_wait[_id] = _temp_event
        self.ws.send(data=data.json())
        _temp_event.wait(timeout=self.timeout)
        return self._config_reply_wait.pop(_id)

    def _config_ready(self, _id: str, data):
        """Check if someone if waiting for config data & send it to them."""
        if _id in self._config_reply_wait:
            _temp_event = self._config_reply_wait.pop(_id)
            self._config_reply_wait[_id] = data
            _temp_event.set()
        else:
            print(f"Config reply: {data.id}")

    def _create_session(self, username, password) -> Union[Dict[str, uuid.UUID], None]:
        # Reuse the the one from Wappsto Rest.
        url = f"https://{self.url}/session"

        rdata = httpx.post(
            url=url,
            headers={"Content-type": "application/json"},
            json={"username": username, "password": password},
        )

        if rdata.status_code >= 300:  # TODO: Simpliefy me!
            try:
                error = json.loads(rdata.text)
            except TypeError:
                error = rdata.text
            self.log.error("Error on creating session:")
            self.log.error(error)
            return None
        rjson = json.loads(rdata.text)
        return rjson["meta"]["id"]

    def _get_ws_link(self) -> str:
        paras = "?" + urllib.parse.urlencode(self.parameters).lower()  # type: ignore
        link = f"wss://{self.url}/websocket/open{paras}"
        self.log.debug(f"Link: {link}")
        return link

    def subscribe(
        self,
        wappsto_type: WappstoService,
        unit_uuid: uuid.UUID,
        callback: Callable[[uuid.UUID, EventStreamSchema], None],
    ):
        """Subscribe a callback to a given UUID change."""
        if not isinstance(unit_uuid, uuid.UUID):
            unit_uuid = uuid.UUID(unit_uuid)
        # UNSURE: add lock?
        self.callback_list[unit_uuid] = callback

        data = RPCRequest(
            method=HttpMethods.PATCH,
            params={
                "url": f"/services/{self.version}/websocket/open/subscription",
                "data": f"/{wappsto_type.value}/{unit_uuid}",
            },
        )

        return self._config_wait(data.id, data)

    def unsubscribe(self, wappsto_type: WappstoService, unit_uuid: uuid.UUID):
        # # remove Subscription & callback
        if not isinstance(unit_uuid, uuid.UUID):
            unit_uuid = uuid.UUID(unit_uuid)

        data = RPCRequest(
            method=HttpMethods.DELETE,
            params={
                "url": f"/services/{self.version}/websocket/open/subscription",
                "data": f"/{wappsto_type.value}/{unit_uuid}",
            },
        )

        self._config_wait(data.id, data)

        return self.callback_list.pop(unit_uuid, None)

    def socket_info(self):
        # # Get Socket Info.
        data = RPCRequest(
            method=HttpMethods.GET,
            params={
                "url": f"/services/{self.version}/websocket/open",
            },
        )

        return self._config_wait(data.id, data)

    def __on_open(self, *args) -> None:
        self.log.debug(f"{self.url} open.")
        self.open = True

    def _default_cb(self, uuid: uuid.UUID, data):
        """Default Callback for the msg. Should not be called."""
        # self._unused_data.append(data)
        self.log.info(f"MSG: {data}")

    def __on_message(self, obj, message, *args) -> None:
        """Store message."""
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print("Error Parsing data.")
            raise

        try:
            data = parse_obj_as(EventStreamSchema, data)
            cb_uuid = data.meta_object.id
        except ValidationError:
            try:
                data = parse_obj_as(RPCSuccess, data)
            except ValidationError:
                print(f"Error Parsing: {data}")
                raise
            else:
                self._config_ready(data.id, data)
                return

        self.log.debug(f"MSG received for: {cb_uuid}")

        # UNSURE: add lock?
        self.callback_list.get(cb_uuid, self._default_cb)(uuid.UUID(cb_uuid), data)

    def __on_error(self, exception, *args, **kwargs) -> None:
        self.log.error(f"exception: {exception}")

    def __on_ping(self, ws, data) -> None:
        self.log.debug("Ping")

    def __on_pong(self, ws, data) -> None:
        self.log.debug("Pong")

    def __on_data(self, ws, data, opcode, finish: bool) -> None:
        self.log.error(f"ws: {ws}")
        self.log.info(f"MSG: {data}")
        self.log.info(f"Code: {opcode}")

    def __on_count(self, ws, data, finish: bool) -> None:
        pass

    def __on_close(self, *args, **kwargs) -> None:
        self.log.info(f"Websocket: {self.url} was closed")

    def close(self):
        # NOTE: There is a 10sec timeout on close, because of the 10sec read timeout.
        self.ws.close()
