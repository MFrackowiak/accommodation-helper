import calendar
from datetime import datetime

from pytz import utc, timezone


def timestamp_from_datetime(datetime_instance: datetime, tz: timezone = utc):
    if not datetime_instance.tzinfo:
        datetime_instance = tz.localize(datetime_instance)

    return calendar.timegm(datetime_instance.astimezone(utc).timetuple())
