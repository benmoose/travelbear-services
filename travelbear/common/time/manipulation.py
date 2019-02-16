from datetime import date, datetime
from typing import Optional


def get_day_from_datetime(dt: datetime) -> Optional[date]:
    """
    >>> dt = datetime(2019, 1, 1, 5, 10, 15)
    >>> get_day_from_datetime(dt)
    datetime.date(2019, 1, 1)
    >>> get_day_from_datetime(None) is None
    True
    """
    if not isinstance(dt, datetime):
        return None
    return date(year=dt.year, month=dt.month, day=dt.day)
