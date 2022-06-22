"""硫化氢传感器数据"""
from datetime import datetime

from ninja import Schema


class H2sBase(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    h2s: int


class H2sIn(H2sBase):
    pass


class H2sOut(H2sBase):
    toilet_name: str


class H2sStatistics(Schema):
    terminal_id: str
    mean_h2s_MEN: int = 0
    max_h2s_MEN: int = 0
    min_h2s_MEN: int = 0
    mean_h2s_WOMEN: int = 0
    max_h2s_WOMEN: int = 0
    min_h2s_WOMEN: int = 0


class H2sStatisticsOut(Schema):
    terminal_id: str
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None

    mean_h2s_MEN: int = 0
    max_h2s_MEN: int = 0
    min_h2s_MEN: int = 0

    mean_h2s_WOMEN: int = 0
    max_h2s_WOMEN: int = 0
    min_h2s_WOMEN: int = 0
