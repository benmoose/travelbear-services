from datetime import datetime
import pytz


def get_current_utc_time():
    return datetime.now(pytz.UTC)
