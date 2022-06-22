import enum

from django.conf import settings

INFLUXDB_URL = settings.INFLUXDB_URL
INFLUXDB_BUCKET = settings.INFLUXDB_BUCKET
INFLUXDB_ORG = settings.INFLUXDB_ORG
INFLUXDB_TOKEN = settings.INFLUXDB_TOKEN

# 设备是否在线间隔，上次通信时间超过该值即为离线 单位分钟
ONLINE_TIMEDELTA = 20


class PeriodEnum(str, enum.Enum):
    EVERY_HOUR = "1h"
    EVERY_DAY = "1d"
    EVERY_MONTH = "1mo"
    # EVERY_YEAR = "1y"
