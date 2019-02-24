from decimal import ROUND_HALF_UP, Decimal
from typing import Optional, Tuple, Union


class InvalidLatLng(ValueError):
    pass


def safe_parse_lat_lng_string(s: str) -> Optional[Tuple[float, float]]:
    """
    >>> safe_parse_lat_lng_string("51.001,-0.123")
    (51.001, -0.123)
    >>> safe_parse_lat_lng_string("  51.5,      -0.1")
    (51.5, -0.1)
    >>> safe_parse_lat_lng_string("0,0")
    (0.0, 0.0)
    >>> safe_parse_lat_lng_string("1,2")
    (1.0, 2.0)
    >>> safe_parse_lat_lng_string("51.0000005,-0.123456789")
    (51.000001, -0.123457)
    >>> safe_parse_lat_lng_string(None)
    >>> safe_parse_lat_lng_string("45,200")
    >>> safe_parse_lat_lng_string("100,10")
    >>> safe_parse_lat_lng_string("1,2,3")
    >>> safe_parse_lat_lng_string("foo")
    >>> safe_parse_lat_lng_string(",")
    >>> safe_parse_lat_lng_string("")
    >>> safe_parse_lat_lng_string(-0.12)
    """
    try:
        return parse_lat_lng_string(s)
    except Exception:  # noqa
        return None


def parse_lat_lng_string(s: str) -> Tuple[float, float]:
    lat, lng = [to_six_dp(v) for v in s.split(",")]
    if not is_valid_latitude(lat):
        raise InvalidLatLng("Latitude must be in range -90 to 90")
    if not is_valid_longitude(lng):
        raise InvalidLatLng("Longitude must be in range -180 to 180")
    return lat, lng


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
    """
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
    """
    return -180 <= lng <= 180


def to_six_dp(n: str) -> float:
    """
    >>> to_six_dp("0.0000005")
    1e-06
    >>> to_six_dp("51.1")
    51.1
    >>> to_six_dp("51.123456")
    51.123456
    >>> to_six_dp("51.123456789")
    51.123457
    >>> to_six_dp("51")
    51.0
    >>> to_six_dp("0")
    0.0
    """
    # use decimal logic to avoid Python rounding weirdness
    return float(Decimal(str(n)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
