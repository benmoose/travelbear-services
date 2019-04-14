from typing import Union


def is_valid_latitude(lat: Union[int, float]) -> bool:
    """
    >>> is_valid_latitude(-90)
    True
    >>> is_valid_latitude(90)
    True
    >>> is_valid_latitude(0)
    True
    >>> is_valid_latitude(-90.1)
    False
    >>> is_valid_latitude(90.1)
    False
    >>> is_valid_latitude(None)
    False
    """
    if not isinstance(lat, (int, float)):
        return False
    return -90 <= lat <= 90


def is_valid_longitude(lng: Union[int, float]) -> bool:
    """
    >>> is_valid_longitude(-180)
    True
    >>> is_valid_longitude(180)
    True
    >>> is_valid_longitude(0)
    True
    >>> is_valid_longitude(-180.1)
    False
    >>> is_valid_longitude(180.1)
    False
    >>> is_valid_longitude(None)
    False
    """
    if not isinstance(lng, (int, float)):
        return False
    return -180 <= lng <= 180
