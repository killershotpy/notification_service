import time

from datetime import timedelta
# from pytz import utc


def get_any_days(value: int = 365):
    return timedelta(days=value)


def now_time_in_int():
    return int(time.time())
