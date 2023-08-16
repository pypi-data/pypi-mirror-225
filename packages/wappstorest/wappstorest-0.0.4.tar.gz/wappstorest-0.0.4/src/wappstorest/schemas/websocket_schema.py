import datetime
import random
import string
import uuid

from enum import Enum

from typing import Any

from pydantic import BaseModel
from pydantic import Extra
from pydantic import validator

from .output.network import Network
from .output.network import Device
from .output.network import Value
from .output.network import State

from .base import BaseMeta
from .base import WappstoVersion


class EventStreamType(str, Enum):
    eventstream = "eventstream"


class MetaEventSchema(BaseModel):
    id: uuid.UUID
    type: EventStreamType
    version: WappstoVersion


class StreamEvents(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    DIRECT = "direct"


class HttpMethods(str, Enum):
    PATCH = "PATCH"
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"


class RpcVersion(str, Enum):
    v2_0 = "2.0"


class EventStreamSchema(BaseModel):
    data: Network | Device | Value | State
    event: StreamEvents
    meta: MetaEventSchema
    meta_object: BaseMeta
    path: str
    timestamp: datetime.datetime

    # @validator('path')
    # def path_check(cls, v, values, **kwargs):
    #     for selftype, selfid in parwise(v.split("/")[1:]):
    #         WappstoMetaType(selftype)
    #         lasttype = selftype
    #         if selfid:
    #             uuid.UUID(selfid)
    #     if "meta_object" in values and "type" in values["meta_object"]:
    #         if values["meta_object"].type != lasttype:
    #             raise ValueError('Path do not match Type')
    #     return v


__session_count: int = 0
__session_id: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))


def _id_gen():
    """Create an unique Rpc-id."""
    global __session_count
    global __session_id
    __session_count += 1
    return f"{__session_id}_WSS_CONFIGS_{__session_count}"


class RPCRequest(BaseModel):
    params: Any | None
    method: HttpMethods
    jsonrpc: RpcVersion | None = RpcVersion.v2_0
    id: str | int | None = None

    class Config:
        extra = Extra.forbid

    @validator("id", pre=True, always=True)
    def id_autofill(cls, v):
        return v or _id_gen()


class RPCSuccess(BaseModel):
    result: Any
    jsonrpc: RpcVersion | None = RpcVersion.v2_0
    id: str | int | None = None

    class Config:
        extra = Extra.forbid

    @validator("id", pre=True, always=True)
    def id_autofill(cls, v):
        return v or _id_gen()
