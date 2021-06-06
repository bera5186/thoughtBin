from uuid import UUID


def is_uuid(uuid: str, version: int = 4) -> bool:
    """
    Check if given string is valid uuid or not

    Parameters
    -----------
    uuid : str
    version : { 1, 2,3, 4}

    Returns
    --------
    `True` if given string is valid uuid, otherwise `False`

    Examples
    ---------
    >>> is_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a)
    True
    >>> is_uuid('xyz')
    False

    """
    try:
        uuid_obj = UUID(uuid, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid
