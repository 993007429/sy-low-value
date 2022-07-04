import uuid
from datetime import date, datetime, timedelta
from math import atan2, cos, degrees, radians, sin, sqrt

from dateutil.tz import tz
from ninja.errors import HttpError

from recycle.models import RegionGrade


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


# 区域范围过滤
def get_zone_range(code):
    code = int(code)
    zone_start = zone_end = code

    if code and code % 1000000000 == 0:
        # 市账号
        zone_end = zone_end + 1000000000
        grade = RegionGrade.CITY
    elif code and code % 1000000 == 0:
        # 区账号
        zone_end = zone_end + 1000000
        grade = RegionGrade.AREA
    elif code and code % 1000 == 0:
        # 街道账号
        zone_end = zone_end + 1000
        grade = RegionGrade.STREET
    else:
        zone_end = zone_start + 1
        grade = RegionGrade.COMMUNITY

    return grade, zone_start, zone_end


# 范围中心确认
def center_geo(locations):
    x, y, z = 0, 0, 0
    lenth = len(locations)
    for lon, lat in locations:
        lon, lat = radians(float(lon)), radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)
    x, y, z = float(x / lenth), float(y / lenth), float(z / lenth)
    lon_center, lat_center = degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y)))
    return lon_center, lat_center
