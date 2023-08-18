from enum import Enum

from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import Extra
from pydantic import UUID4

from .base import WappstoService


class WappstoVersion(Enum):
    V2_0 = "2.0"
    V2_1 = "2.1"


class ApiMetaTypes(Enum):
    IDLIST = "idlist"
    DELETELIST = "deletelist"
    ATTRIBUTELIST = "attributelist"


class ApiMetaInfo(BaseModel):
    type: ApiMetaTypes  # Merge with MetaAPIData?
    version: WappstoVersion


class IdListMeta(BaseModel):
    type: Literal['idlist']
    version: WappstoVersion


class DeleteListMeta(BaseModel):
    type: Literal['deletelist']
    version: WappstoVersion


class childInfo(BaseModel):
    type: WappstoService
    version: WappstoVersion


class IdList(BaseModel):
    child: list[ApiMetaInfo]
    id: list[UUID4]
    more: bool
    limit: int
    count: int
    meta: IdListMeta


class DeleteList(BaseModel):
    deleted: list[UUID4]
    code: int
    message: str = "Deleted"
    meta: DeleteListMeta

    # TODO: Remove: 'Extra.forbid' and use meta->type to force type.


class AttributeList(BaseModel):
    data: dict[UUID4, Any]
    more: bool
    path: str
    meta: ApiMetaInfo
