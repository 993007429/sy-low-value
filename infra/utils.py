import uuid
from datetime import date, datetime, timedelta

from dateutil.tz import tz
from ninja.errors import HttpError


def uuid1():
    return uuid.uuid1().hex


cn = tz.gettz("Asia/Shanghai")


def now_tz_aware():
    return DatetimeISO.now(tz=cn)


class DatetimeISO(datetime):
    def __str__(self):
        return self.isoformat()


def local_datetime_iso():
    return DatetimeISO.now(tz=cn).replace(hour=0, minute=0, second=0, microsecond=0)


def to_local_datetime(dt: date):
    return DatetimeISO(dt.year, dt.month, dt.day, hour=0, minute=0, second=0, microsecond=0, tzinfo=cn)


def to_time_range_tz(start_date: date, end_date: date, raise_exception: bool = True) -> (DatetimeISO, DatetimeISO):
    if not start_date:
        start_date = local_datetime_iso()
    else:
        start_date = to_local_datetime(start_date)
    if not end_date:
        end_date = local_datetime_iso()
    else:
        end_date = to_local_datetime(end_date)
    end_date = end_date + timedelta(days=1)

    if start_date >= end_date and raise_exception:
        raise HttpError(400, "开始时间应小于结束时间")

    return start_date, end_date
