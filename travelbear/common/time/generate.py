from datetime import datetime

import pytz


def get_current_utc_time():
    """
    >>> type(get_current_utc_time())
    <class 'datetime.datetime'>
    """
    return datetime.now(pytz.UTC)
