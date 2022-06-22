"""电表传感器数据"""
from datetime import datetime

from ninja import Schema


class AmmeterBase(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    kwh: float


class AmmeterIn(AmmeterBase):
    pass


class AmmeterOut(AmmeterBase):
    toilet_name: str


class AmmeterStatistics(Schema):
    terminal_id: str
    kwh: float = 0


class AmmeterStatisticsOut(Schema):
    terminal_id: str
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None
    kwh: float = 0
