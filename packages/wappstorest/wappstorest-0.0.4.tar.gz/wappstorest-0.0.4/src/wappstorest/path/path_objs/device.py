from ..path_helpers import Wrapper


class StateWarningItem:
    __path__ = 'device.value.state.meta.warning'
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
    __path__ = 'device.value.state.meta'
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
    __path__ = 'device.value.state'
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
    __path__ = 'device.value.meta.warning'
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
    __path__ = 'device.value.meta'
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
    __path__ = 'device.value.info'
    overrite_list = [
        'enabled',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Number:
    __path__ = 'device.value.number'
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
    __path__ = 'device.value.string'
    overrite_list = [
        'max',
        'encoding',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Blob:
    __path__ = 'device.value.blob'
    overrite_list = [
        'max',
        'encoding',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Xml:
    __path__ = 'device.value.xml'
    overrite_list = [
        'xsd',
        'namespace',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class ValueEventlogWarningItem:
    __path__ = 'device.value.eventlog.meta.warning'
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
    __path__ = 'device.value.eventlog.meta'
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
    __path__ = 'device.value.eventlog'
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
    __path__ = 'device.value'
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
    __path__ = 'device.meta.geo'
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
    __path__ = 'device.meta.warning'
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
    __path__ = 'device.meta'
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
    __path__ = 'device.status.meta'
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
    __path__ = 'device.status'
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
    __path__ = 'device.info'
    overrite_list = [
        'enabled',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Device:
    __path__ = 'device'
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
    status = Status
    value = Value
    info = DeviceInfo
