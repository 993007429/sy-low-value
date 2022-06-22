"""氨气传感器数据"""
from datetime import datetime

from ninja import Schema


class Nh3Base(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    nh3: int


class Nh3In(Nh3Base):
    pass


class Nh3Out(Nh3Base):
    toilet_name: str


class Nh3Statistics(Schema):
    terminal_id: str
    mean_nh3_MEN: int = 0
    max_nh3_MEN: int = 0
    min_nh3_MEN: int = 0
    mean_nh3_WOMEN: int = 0
    max_nh3_WOMEN: int = 0
    min_nh3_WOMEN: int = 0


class Nh3StatisticsOut(Schema):
    terminal_id: str
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None

    mean_nh3_MEN: int = 0
    max_nh3_MEN: int = 0
    min_nh3_MEN: int = 0

    mean_nh3_WOMEN: int = 0
    max_nh3_WOMEN: int = 0
    min_nh3_WOMEN: int = 0
