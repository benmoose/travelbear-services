from datetime import datetime
import pytz

from .current_utc_time import current_utc_time


def test_current_utc_time():
    current_time = current_utc_time()
    assert isinstance(current_time, datetime)
    assert current_time.tzinfo == pytz.UTC
