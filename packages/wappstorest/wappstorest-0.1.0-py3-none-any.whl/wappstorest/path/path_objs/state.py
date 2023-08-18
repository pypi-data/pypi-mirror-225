from ..path_helpers import Wrapper


class Meta:
    __path__ = 'state.meta'
    overrite_list = [
        'id',
        'trace',
        'redirect',
        'icon',
        'tag',
        'tag_by_user',
        'name_by_user',
        'historical',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class State:
    __path__ = 'state'
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

    meta = Meta
