"""客流量传感器数据"""
from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import Field


class PassengerVolumeBase(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    volume: int


class PassengerVolumeIn(PassengerVolumeBase):
    pass


class PassengerVolumeOut(PassengerVolumeBase):
    toilet_name: str


class PassengerVolumeStatistics(Schema):
    terminal_id: str
    volume: int = 0


class PassengerVolumeStatisticsOut(Schema):
    terminal_id: str
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None
    volume: int


class PassengerVolumeRealtimeInfoOut(Schema):
    terminal_id: str
    volume: int = 0


class PassengerVolumeWindowMean(Schema):
    time: datetime = Field(..., alias="_time", description="采样时间")
    passenger_volume: int = Field(None, alias="volume", description="人流量")


class PassengerVolumeWindowMeanOut(Schema):
    terminal_id: str
    toilet_name: str = None

    data: List[PassengerVolumeWindowMean]


class BatchPassengerVolumeLastHourMean(Schema):
    terminal_id: str = None
    passenger_volume: int = Field(None, alias="_value", description="人流量")


class BatchPassengerVolumeLastHourMeanOut(BatchPassengerVolumeLastHourMean):
    toilet_name: str = None
    code: str = None
    time: datetime
