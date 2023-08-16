import datetime

from enum import Enum
from pydantic import BaseModel
from pydantic import constr
from pydantic import UUID4

from typing import Any

from ..core.utils import timestamp


class WappstoEnv(Enum):
    """Wappstos difference environments."""
    PROD = 'prod'
    QA = 'qa'
    DEV = 'dev'
    STAGING = 'staging'


class WappstoService(Enum):
    """Wappstos difference Services."""
    ACL = "acl"
    ADD_NOT_OWNED = "add_not_owned"
    ADMIN_FEATURE = "admin_feature"
    ALERT = "alert"
    ANALYTICS = "analytics"
    ANALYTICS_MODEL = "analytics_model"
    API = "api"
    APPLICATION = "application"
    APPLICATION_PRODUCT = "application_product"
    ASYNCHRONOUS = "asynchronous"
    ATTRIBUTELIST = "attributelist"
    AZURE = "azure"
    BACKGROUND = "background"
    BAN_LIST = "ban_list"
    BUS_STREAM = "bus_stream"
    CLEANUP_HISTORICAL = "cleanup_historical"
    COCKROACH = "cockroach"
    CONSOLE = "console"
    COUCHBASE = "couchbase"
    COUNTER = "counter"
    CREATOR = "creator"
    CUSTOMER = "customer"
    CUSTOMER_INVOICE = "customer_invoice"
    DASHBOARD = "dashboard"
    DATA = "data"
    DEBUGGER = "debugger"
    DELETELIST = "deletelist"
    DEVICE = "device"
    DOWNLOAD = "download"
    EMAIL = "email"
    EMAIL_DRAFT = "email_draft"
    EMAIL_SEND = "email_send"
    EMAIL_TRANSLATION = "email_translation"
    ERROR = "error"
    EVENTLOG = "eventlog"
    EVENTSTREAM = "eventstream"
    EXPECTED_STATE = "expected_state"
    EXTSYNC = "extsync"
    EXTSYNC_RESPONSE = "extsync_response"
    FETCH = "fetch"
    FILE = "file"
    FILTER = "filter"
    FIRMWARE = "firmware"
    FITE = "fite"
    HOMEPAGE = "homepage"
    HTTPRESPONSE = "httpresponse"
    ICON = "icon"
    IDLIST = "idlist"
    INSTALLATION = "installation"
    INVOICE = "invoice"
    LOG = "log"
    LOG_ZIP = "log_zip"
    MDA = "mda"
    META = "meta"
    METRICS = "metrics"
    MICRO = "micro"
    MODBUS = "modbus"
    MQTT = "mqtt"
    N1QL = "n1ql"
    NATS = "nats"
    NETWORK = "network"
    NOTIFICATION = "notification"
    OAUTH = "oauth"
    OAUTH_CLIENT = "oauth_client"
    OAUTH_CONNECT = "oauth_connect"
    OAUTH_EXTERNAL = "oauth_external"
    ONTOLOGY = "ontology"
    PARSER = "parser"
    PENDING_USER = "pending_user"
    PERMISSION = "permission"
    PERMISSION_GROUP = "permission_group"
    PERMISSION_RULE = "permission_rule"
    POINT = "point"
    PRICE = "price"
    PROCESS = "process"
    PRODUCT = "product"
    PROMOTE = "promote"
    PROTOTYPE = "prototype"
    PURSE = "purse"
    PURSE_APPLICATION = "purse_application"
    QUERY = "query"
    RECOVERY = "recovery"
    RECOVERY_CLEANUP = "recovery_cleanup"
    RECOVERY_REPEAT = "recovery_repeat"
    REGISTER = "register"
    REPEAT = "repeat"
    RPC_ERROR = "rpc_error"
    RPC_REQUEST = "rpc_request"
    RPC_RESULT = "rpc_result"
    SCHEMA = "schema"
    SEARCH = "search"
    SELLER = "seller"
    SESSION = "session"
    SMS = "sms"
    SMS_DRAFT = "sms_draft"
    SMS_SEND = "sms_send"
    STATE = "state"
    STATUS = "status"
    STORAGE = "storage"
    STREAM = "stream"
    STRIPE = "stripe"
    SUBSCRIPTION = "subscription"
    SUBUSER = "subuser"
    SUMMARY = "summary"
    TAX = "tax"
    TRANSFER_BILLING = "transfer_billing"
    TRANSFER_EMAIL = "transfer_email"
    TRANSFER_TRANSLATION = "transfer_translation"
    TRANSFER_USER = "transfer_user"
    USER = "user"
    VALUE = "value"
    VERSION = "version"
    VIRTUALUSER = "virtualuser"
    WEBSOCKET = "websocket"
    WIDGET = "widget"


class WappstoVersion(Enum):
    V2_0 = "2.0"
    V2_1 = "2.1"


class ApiMetaTypes(Enum):
    # TODO: Add all services from WappstoService to this.
    idlist = "idlist"
    deletelist = "deletelist"


class Deletion(str, Enum):
    PENDING = 'pending'
    FAILED = 'failed'


class Assigned(str, Enum):
    UNASSIGNED = 'unassigned'


class ApiMetaInfo(BaseModel):
    type: ApiMetaTypes  # Merge with MetaAPIData?
    version: WappstoVersion


class WarningItem(BaseModel):
    message: str | None = None
    data: dict[str, Any] | None = None
    code: int | None = None


class BaseMeta(BaseModel):  # Base Meta
    id: UUID4 | None = None
    # NOTE: Set in the children-class.
    # #  type: Optional[WappstoMetaType] = None
    version: WappstoVersion | None = None

    manufacturer: UUID4 | None = None
    owner: UUID4 | Assigned | None = None
    parent: UUID4 | None = None

    created: datetime.datetime | None = None
    updated: datetime.datetime | None = None
    changed: datetime.datetime | None = None

    application: UUID4 | None = None
    deletion: Deletion | None = None
    deprecated: bool | None = None

    iot: bool | None = None
    revision: int | None = None
    size: int | None = None
    path: str | None = None

    oem: str | None = None
    accept_manufacturer_as_owner: bool | None = None
    redirect: constr(  # type: ignore
        regex=r'^[0-9a-zA-Z_-]+$',  # noqa: F722
        min_length=1,
        max_length=200
    ) | None = None

    error: UUID4 | None = None
    warning: list[WarningItem] | None = None
    trace: str | None = None

    set: list[UUID4] | None = None
    contract: list[UUID4] | None = None

    historical: bool | None = None

    class Config:
        json_encoders = {
            datetime: timestamp
        }
