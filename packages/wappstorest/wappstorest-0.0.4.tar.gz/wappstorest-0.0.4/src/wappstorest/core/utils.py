import datetime


def timestamp(dt: datetime.datetime) -> str:
    """
    Return The default timestamp used for Wappsto.

    The timestamp are always set to the UTC timezone.

    Returns:
        The UTC time string in ISO format.
    """
    return dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
