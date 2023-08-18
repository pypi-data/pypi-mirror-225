from ..path_helpers import Wrapper


class ProviderItem():
    __path__ = 'user.provideritem'
    overrite_list = [
        'name',
        'picture',
        'type',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class OtherEmailItem:
    __path__ = 'user.otheremailitem'
    overrite_list = [
        'contact',
        'status',
        'last_update',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class OtherSm:
    __path__ = 'user.othersm'
    overrite_list = [
        'contact',
        'status',
        'last_update',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Ban:
    __path__ = 'user.ban'
    overrite_list = [
        'type',
        'begin_ban',
        'end_ban',
        'motivation',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )


class Meta:
    __path__ = 'user.meta'
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


class User:
    __path__: str = 'user'
    overrite_list = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'name',
        'role',
        'nickname',
        'language',
        'friend',
        'blocked',
        'verified_email',
        'verified_sms',
        'admin',
        'founder',
    ]
    for tmpop8yroywhfgkljsdyekj_name in overrite_list:
        locals()[tmpop8yroywhfgkljsdyekj_name] = Wrapper(
            tmpop8yroywhfgkljsdyekj_name, __path__
        )

    provider = ProviderItem
    other_email = OtherEmailItem
    other_sms = OtherSm
    ban = Ban
    meta = Meta
