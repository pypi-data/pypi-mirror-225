from ..path_helpers import Wrapper


class WarningItem:
    __path__ = 'session.meta.warning'
    overrite_list = [
        'message',
        'data',
        'code',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Meta:
    __path__ = 'session.meta'
    overrite_list = [
        'id',
        'type',
        'version',
        'manufacturer',
        'owner',
        'created',
        'updated',
        'changed',
        'application',
        'revision',
        'trace',
        'oem',
        'deprecated',
        'redirect',
        'size',
        'path',
        'parent',
        'error',
        'icon',
        'tag',
        'tag_by_user',
        'name_by_user',
        'parent_name',
        'read_only',
        'original_id',
        'alert',
        'contract',
    ]

    warning = WarningItem


class Session:
    __path__ = 'session'
    overrite_list = [
        'username',
        'remember_me',
        'system',
        'provider',
        'type',
        'installation',
        'admin',
        'dashboard',
        'test_mode',
        'theme',
        'user',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    meta = Meta
