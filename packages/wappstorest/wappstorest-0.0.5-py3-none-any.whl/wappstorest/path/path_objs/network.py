from ..path_helpers import Wrapper


class StateWarningItem:
    __path__ = 'network.device.value.state.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class StateMeta:
    __path__ = 'network.device.value.state.meta'
    overrite_list = [
        'type',
        'id',
        'version',
        'manufacturer',
        'owner',
        'parent',
        'created',
        'updated',
        'changed',
        'application',
        'deprecated',
        'iot',
        'revision',
        'size',
        'path',
        'oem',
        'accept_manufacturer_as_owner',
        'redirect',
        'error',
        'trace',
        'set',
        'contract',
        'historical',
        'deletion',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    warning = StateWarningItem


class State:
    __path__ = 'network.device.value.state'
    overrite_list = [
        'timestamp',
        'data',
        'type',
        'status',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    meta = StateMeta


class ValueWarningItem:
    __path__ = 'network.device.value.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class ValueMeta:
    __path__ = 'network.device.value.meta'
    overrite_list = [
        'type',
        'id',
        'version',
        'manufacturer',
        'owner',
        'parent',
        'created',
        'updated',
        'changed',
        'application',
        'deprecated',
        'iot',
        'revision',
        'size',
        'path',
        'oem',
        'accept_manufacturer_as_owner',
        'redirect',
        'error',
        'trace',
        'set',
        'contract',
        'historical',
        'deletion',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    warning = ValueWarningItem


class ValueInfo:
    __path__ = 'network.device.value.info'
    overrite_list = [
        'enabled',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Number:
    __path__ = 'network.device.value.number'
    overrite_list = [
        'min',
        'max',
        'step',
        'mapping',
        'meaningful_zero',
        'ordered_mapping',
        'si_conversion',
        'unit',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class String:
    __path__ = 'network.device.value.string'
    overrite_list = [
        'max',
        'encoding',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Blob:
    __path__ = 'network.device.value.blob'
    overrite_list = [
        'max',
        'encoding',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Xml:
    __path__ = 'network.device.value.xml'
    overrite_list = [
        'xsd',
        'namespace',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class ValueEventlogWarningItem:
    __path__ = 'network.device.value.eventlog.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class ValueEventlogMeta:
    __path__ = 'network.device.value.eventlog.meta'
    overrite_list = [
        'type',
        'id',
        'version',
        'manufacturer',
        'owner',
        'parent',
        'created',
        'updated',
        'changed',
        'application',
        'deprecated',
        'iot',
        'revision',
        'size',
        'path',
        'oem',
        'accept_manufacturer_as_owner',
        'redirect',
        'error',
        'trace',
        'set',
        'contract',
        'historical',
        'deletion',
        'icon',
        'alert',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    warning = ValueEventlogWarningItem


class ValueEventlogItem:
    __path__ = 'network.device.value.eventlog'
    overrite_list = [
        'message',
        'timestamp',
        'info',
        'level',
        'type',
    ]

    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    meta = ValueEventlogMeta


class Value:
    __path__ = 'network.device.value'
    overrite_list = [
        'name',
        'type',
        'description',
        'period',
        'delta',
        'permission',
        'status',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    meta = ValueMeta
    state = State
    eventlog = ValueEventlogItem
    info = ValueInfo
    string = String
    number = Number
    blob = Blob
    xml = Xml


class DeviceGeo:
    __path__ = 'network.device.meta.geo'
    overrite_list = [
        'latitude',
        'longitude',
        'display_name',
        'address',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class DeviceWarningItem:
    __path__ = 'network.device.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class DeviceMeta:
    __path__ = 'network.device.meta'
    overrite_list = [
        'type',
        'id',
        'version',
        'manufacturer',
        'owner',
        'parent',
        'created',
        'updated',
        'changed',
        'application',
        'deprecated',
        'iot',
        'revision',
        'size',
        'path',
        'oem',
        'accept_manufacturer_as_owner',
        'redirect',
        'error',
        'trace',
        'set',
        'contract',
        'historical',
        'deletion',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    warning = DeviceWarningItem

    geo = DeviceGeo


class StatusMeta:
    __path__ = 'network.device.status.meta'
    overrite_list = [
        'type',
        'id',
        'version',
        'manufacturer',
        'owner',
        'parent',
        'created',
        'updated',
        'changed',
        'application',
        'deprecated',
        'iot',
        'revision',
        'size',
        'path',
        'oem',
        'accept_manufacturer_as_owner',
        'redirect',
        'error',
        'trace',
        'set',
        'contract',
        'historical',
        'deletion',
        'icon',
        'alert',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    warning = ValueEventlogWarningItem


class Status:
    __path__ = 'network.device.status'
    overrite_list = [
        'message',
        'timestamp',
        'data',
        'type',
        'level',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    meta = StatusMeta


class DeviceInfo:
    __path__ = 'network.device.info'
    overrite_list = [
        'enabled',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Device:
    __path__ = 'network.device'
    overrite_list = [
        'name',
        'control_timeout',
        'control_when_offline',
        'manufacturer',
        'product',
        'version',
        'serial',
        'description',
        'protocol',
        'communication',
        'included',
        'inclusion_status',
        'firmware_status',
        'firmware_upload_progress',
        'firmware_available_version',
        'command',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    meta = DeviceMeta
    status: Status
    value: Value
    info = DeviceInfo


class NetworkWarningItem:
    __path__ = 'network.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class NetworkGeo:
    __path__ = 'network.meta.geo'
    overrite_list = [
        'latitude',
        'longitude',
        'display_name',
        'address',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Connection:
    __path__ = 'network.meta.connection'
    overrite_list = [
        'timestamp',
        'online',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class NetworkMeta:
    __path__ = 'network.meta'
    overrite_list = [
        'id',
        'version',
        'manufacturer',
        'owner',
        'parent',
        'created',
        'updated',
        'changed',
        'application',
        'deletion',
        'deprecated',
        'iot',
        'revision',
        'size',
        'path',
        'oem',
        'accept_manufacturer_as_owner',
        'redirect',
        'error',
        'trace',
        'set',
        'contract',
        'historical',
        'accept_test_mode',
        'verify_product',
        'product',
    ]

    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    warning = NetworkWarningItem
    geo = NetworkGeo
    connection = Connection


class NetworkInfo:
    __path__ = 'network.info'
    overrite_list = [
        'enabled',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Network:
    __path__ = 'network'
    overrite_list = [
        'name',
        'description',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )
    name: str | None = None
    description: str | None = None

    info = NetworkInfo
    device = Device
    meta = NetworkMeta
