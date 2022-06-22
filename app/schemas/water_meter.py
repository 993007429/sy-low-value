"""水表传感器数据"""
from datetime import datetime

from ninja import Schema


class WaterMeterBase(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    volume: float


class WaterMeterIn(WaterMeterBase):
    pass


class WaterMeterOut(WaterMeterBase):
    toilet_name: str


class WaterMeterStatistics(Schema):
    terminal_id: str
    volume: int = 0


class WaterMeterStatisticsOut(Schema):
    terminal_id: str
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None
    volume: int = 0


class WaterMeterRealtimeInfoOut(Schema):
    terminal_id: str
    kwh: float = 0
    volume: float = 0
