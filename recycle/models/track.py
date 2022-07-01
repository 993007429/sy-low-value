from datetime import datetime

from influxdb_client import Point
from pydantic import BaseModel, Field


class Track(BaseModel):
    """车辆轨迹，包括经纬度、速度、方向等"""

    plate_number: str = Field(title="车牌号", max_length=32)
    tracked_at: datetime = Field(title="定位时间")
    phone: str = Field(title="手机号", max_length=16)
    longitude: float = Field(title="经度")
    latitude: float = Field(title="纬度")
    altitude: float = Field(title="海拔(米)")
    speed: int = Field(title="速度")
    direction: int = Field(title="方向")

    def to_data_point(self) -> Point:
        return (
            Point("track")
            .time(self.tracked_at)
            .tag("plate_number", self.plate_number)
            .tag("phone", self.phone)
            .field("longitude", self.longitude)
            .field("latitude", self.latitude)
            .field("altitude", self.altitude)
            .field("speed", self.speed)
            .field("direction", self.direction)
        )
