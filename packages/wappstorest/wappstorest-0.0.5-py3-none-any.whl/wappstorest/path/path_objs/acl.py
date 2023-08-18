from ..path_helpers import Wrapper


class Application:
    __path__: str = 'acl.permissionitem.restrictionitem.application'
    overrite_list = [
        'sharing',
        'permitted',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Method:
    __path__: str = 'acl.permissionitem.restrictionitem.method'
    overrite_list = [
        'create',
        'update',
        'retrieve',
        'delete',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class State:
    __path__: str = 'acl.permissionitem.restrictionitem.state'
    overrite_list = [
        'min_state',
        'max_state',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Installation:
    __path__: str = 'acl.permissionitem.restrictionitem.installation'
    overrite_list = [
        'shareable'
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class File:
    __path__: str = 'acl.permissionitem.restrictionitem.file'
    overrite_list = [
        'background'
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class RestrictionItem:
    __path__: str = 'acl.permissionitem.restrictionitem'
    overrite_list = [
        'child',
        'create',
        'time',
        'acl_attributes',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    application = Application
    file = File
    installation = Installation
    method = Method
    state = State


class Meta:
    __path__: str = 'acl.permissionitem.meta'
    overrite_list = [
        'id',
        'trace',
        'redirect',
        'icon',
        'tag',
        'tag_by_user',
        'name_by_user',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class PermissionItem:
    __path__: str = 'acl.permissionitem'
    overrite_list = [
        'name',
        'message',
        'propagate',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    restriction = RestrictionItem
    meta = Meta


class Meta1:
    __path__: str = 'acl.meta'
    overrite_list = [
        'id',
        'trace',
        'redirect',
        'icon',
        'tag',
        'tag_by_user',
        'name_by_user',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Acl:
    __path__: str = 'acl'
    overrite_list = [
        'owner',
        'manufacturer',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    permission = PermissionItem
    meta = Meta1
