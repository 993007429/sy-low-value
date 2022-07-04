from datetime import datetime

from ninja import Schema
from pydantic import Field


class TrackBase(Schema):
    plate_number: str = Field(title="车牌号", max_length=32)
    tracked_at: datetime = Field(title="定位时间")
    phone: str = Field(title="手机号", max_length=16)
    longitude: float = Field(title="经度")
    latitude: float = Field(title="纬度")
    altitude: float = Field(title="海拔(米)")
    speed: float = Field(title="速度")
    direction: int = Field(title="方向")


class TrackIn(TrackBase):
    pass


class TrackOut(Schema):
    plate_number: str = Field(title="车牌号", max_length=32)
    tracked_at: datetime = Field(title="定位时间", alias="_time")
    longitude: float = Field(title="经度")
    latitude: float = Field(title="纬度")
