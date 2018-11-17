from datetime import datetime


RFC_3339_FORMAT_STRING_WITH_MICROSECONDS = '%Y-%m-%dT%H:%M:%S.%f%z'
RFC_3339_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S%z'


def safe_parse_rfc_3339(time_string):
    """
    >>> isinstance(safe_parse_rfc_3339('2018-01-01T10:00:00.52Z'), datetime)
    True
    >>> safe_parse_rfc_3339('2018-01-01T10:00:00.52Z')
    datetime.datetime(2018, 1, 1, 10, 0, 0, 520000, tzinfo=datetime.timezone.utc)
    >>> safe_parse_rfc_3339('2018-01-01T10:00:58-06:00')
    datetime.datetime(2018, 1, 1, 10, 0, 58, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=64800)))
    >>> safe_parse_rfc_3339('2018-05-10') is None
    True
    >>> safe_parse_rfc_3339('malformed $h14') is None
    True
    >>> safe_parse_rfc_3339('2018-01-01T00:00:00') is None
    True
    >>> safe_parse_rfc_3339(None) is None
    True
    """
    if not isinstance(time_string, str):
        return None

    for fs in [RFC_3339_FORMAT_STRING_WITH_MICROSECONDS, RFC_3339_FORMAT_STRING]:
        try:
            dt = datetime.strptime(time_string, fs)
            if dt.tzinfo is None:
                return None
            return dt
        except ValueError:
            continue
