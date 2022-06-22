"""厕位传感器"""
from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import Field

from app.models.sensors import InstallationLocation


class Seat(Schema):
    sensor_id: str = Field(..., description="厕位传感器")
    occupied: bool = Field(..., description="厕位是否有人")


class ToiletSeatIn(Schema):
    terminal_id: str
    gather_time: datetime
    seats: List[Seat]


class SeatState(Schema):
    seat: str = Field(..., description="厕位号")
    occupied: bool = Field(..., description="厕位是否有人")


class ToiletSeatOut(Schema):
    terminal_id: str
    toilet_name: str
    sensor_id: str
    seat_serial: int = Field(None, description="坑位序号")
    gather_time: datetime
    installation_location: InstallationLocation
    occupied: int = Field(..., description="是否有人，0无人 1有人")


class ToiletSeatStatistics(Schema):
    terminal_id: str
    MEN: int = Field(0, description="男厕使用次数")
    WOMEN: int = Field(0, description="女厕使用次数")
    GENDERLESS: int = Field(0, description="无差卫生间使用次数")


class ToiletSeatStatisticsOut(ToiletSeatStatistics):
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None


class ToiletSeatRealtimeInfoOut(Schema):
    terminal_id: str
    MEN_toilet_occupied: int = Field(0, alias="MEN")
    WOMEN_toilet_occupied: int = Field(0, alias="WOMEN")
    GENDERLESS_toilet_occupied: int = Field(0, alias="GENDERLESS")
