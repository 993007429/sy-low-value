import dataclasses
from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from influxdb_client import Point

from infra.const import ONLINE_TIMEDELTA
from infra.db.models import BaseModel
from infra.utils import now_tz_aware


class SensorType(models.TextChoices):
    PASSENGER_VOLUME = "PASSENGER_VOLUME", "客流检测仪"
    H2S = "H2S", "硫化氢监测仪"
    NH3 = "NH3", "氨气监测仪"
    MANAGEMENT_TERMINAL = "MANAGEMENT_TERMINAL", "公厕智能管理终端"
    TOILET_SEAT = "TOILET_SEAT", "坑位状态监测仪"
    AIR_QUALITY = "AIR_QUALITY", "空气质量监测仪"
    AMMETER = "AMMETER", "电表"
    WATER_METER = "WATER_METER", "水表"
    BLUETOOTH_REPEATER = "BLUETOOTH_REPEATER", "蓝牙中继器"
    OTHERS = "OTHERS", "其他"


class InstallationLocation(models.TextChoices):
    MEN = "MEN", "男厕"
    WOMEN = "WOMEN", "女厕"
    GENDERLESS = "GENDERLESS", "无差别卫生间"
    ENTRY = "ENTRY", "门口"
    OTHERS = "OTHERS", "其他"


class Sensor(BaseModel):
    """传感器"""

    sensor_id = models.CharField("传感器编号", max_length=32, unique=True)
    sensor_type = models.CharField("传感器类型", max_length=32, choices=SensorType.choices)
    toilet = models.ForeignKey("Toilet", on_delete=models.CASCADE, db_constraint=False)
    installation_location = models.CharField("安装位置", max_length=32, choices=InstallationLocation.choices)
    serial = models.PositiveSmallIntegerField("厕位序号", null=True, blank=True, help_text="只有传感器类型是坑位传感器时才有效")
    last_communication_time = models.DateTimeField("最后通信时间", null=True, blank=True)

    @staticmethod
    def update_last_communication_time(sensor_id: str, dt: datetime = None):
        if dt is None:
            dt = timezone.now()
        Sensor.objects.filter(sensor_id=sensor_id).update(last_communication_time=dt)

    @property
    def is_online(self):
        # 最后通信时间超过10分钟就是离线
        if not self.last_communication_time:
            return False
        return now_tz_aware() - self.last_communication_time < timedelta(minutes=ONLINE_TIMEDELTA)  # noqa


@dataclasses.dataclass
class AirQuality:
    """空气质量"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    temperature: float
    humidity: float
    pm2_5: int
    pm10: int
    co2: int
    installation_location: str = None

    def to_data_point(self) -> Point:
        return (
            Point("air_quality")
            # .time(self.gather_time) # 物联网卡联网受限制，不能同步时间服务器，使用服务器时间吧。
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .tag("installation_location", self.installation_location)
            .field("temperature", self.temperature)
            .field("humidity", self.humidity)
            .field("pm2_5", self.pm2_5)
            .field("pm10", self.pm10)
            .field("co2", self.co2)
        )


@dataclasses.dataclass
class H2s:
    """硫化氢"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    h2s: int
    installation_location: str = None

    def to_data_point(self) -> Point:
        return (
            Point("h2s")
            # .time(self.gather_time)
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .tag("installation_location", self.installation_location)
            .field("h2s", self.h2s)
        )


@dataclasses.dataclass
class Nh3:
    """氨气"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    nh3: int
    installation_location: str = None

    def to_data_point(self) -> Point:
        return (
            Point("nh3")
            # .time(self.gather_time)
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .tag("installation_location", self.installation_location)
            .field("nh3", self.nh3)
        )


@dataclasses.dataclass
class Ammeter:
    """电表"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    kwh: float

    def to_data_point(self) -> Point:
        return (
            Point("ammeter")
            # .time(self.gather_time)
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .field("kwh", self.kwh)
        )


@dataclasses.dataclass
class WaterMeter:
    """水表"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    volume: float

    def to_data_point(self) -> Point:
        return (
            Point("water_meter")
            # .time(self.gather_time)
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .field("volume", self.volume)
        )


@dataclasses.dataclass
class PassengerVolume:
    """客流量"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    volume: float

    def to_data_point(self) -> Point:
        return (
            Point("passenger_volume")
            # .time(self.gather_time)
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .field("volume", self.volume)
        )


@dataclasses.dataclass
class ToiletSeat:
    """厕位"""

    toilet_name: str
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    occupied: int  # 有人1 无人0,不用bool是为了方便统计使用次数
    installation_location: str = None
    seat_serial: int = None

    def to_data_point(self) -> Point:
        return (
            Point("toilet_seat")
            .time(self.gather_time)
            .tag("toilet_name", self.toilet_name)
            .tag("terminal_id", self.terminal_id)
            .tag("sensor_id", self.sensor_id)
            .tag("installation_location", self.installation_location)
            .tag("seat_serial", self.seat_serial)
            .field("occupied", self.occupied)
        )


class WorkCardScan(BaseModel):
    """工牌扫描记录"""

    work_card = models.CharField("工牌", max_length=64)
    toilet = models.ForeignKey("Toilet", db_constraint=False, on_delete=models.SET_NULL, null=True)
