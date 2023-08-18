from ..path_helpers import Wrapper


class ValueWarningItem:
    __path__ = 'value.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class StateWarningItem:
    __path__ = 'value.state.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class EventlogWarningItem:
    __path__ = 'value.eventlog.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class EventlogMeta:
    __path__ = 'value.eventlog.meta'
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

    warning = EventlogWarningItem


class ValueMeta:
    __path__ = 'value.meta'
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


class Info:
    __path__ = 'value.info'
    overrite_list = [
        'enabled',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class StateMeta:
    __path__ = 'value.state.meta'
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
    __path__ = 'value.state'
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


class ValueEventlogItem:
    __path__ = 'value.eventlog'
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

    meta = EventlogMeta


class Number:
    __path__ = 'value.number'
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
    __path__ = 'value.string'
    overrite_list = [
        'max',
        'encoding',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Blob:
    __path__ = 'value.blob'
    overrite_list = [
        'max',
        'encoding',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Xml:
    __path__ = 'value.xml'
    overrite_list = [
        'xsd',
        'namespace',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Value:
    __path__ = 'value'
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
    eventlog = EventlogItem
    info = Info
    string = String
    number = Number
    blob = Blob
    xml = Xml
