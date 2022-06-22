"""空气质量传感器数据，包括温度、湿度、pm2.5、pm10、二氧化碳等"""
from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import Field


class AirQualityBase(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    temperature: float
    humidity: float
    pm2_5: int
    pm10: int
    co2: int


class AirQualityIn(AirQualityBase):
    pass


class AirQualityOut(AirQualityBase):
    toilet_name: str
    installation_location: str = None


class AirQualityStatistics(Schema):
    terminal_id: str

    temperature_MEN: float = 0
    humidity_MEN: float = 0
    pm2_5_MEN: int = 0
    pm10_MEN: int = 0
    co2_MEN: int = 0

    temperature_WOMEN: float = 0
    humidity_WOMEN: float = 0
    pm2_5_WOMEN: int = 0
    pm10_WOMEN: int = 0
    co2_WOMEN: int = 0


class AirQualityStatisticsOut(Schema):
    terminal_id: str
    toilet_name: str = None
    toilet_type: str = None
    organization_id: int = None
    organization_name: str = None

    temperature_MEN: float = 0
    humidity_MEN: float = 0
    pm2_5_MEN: int = 0
    pm10_MEN: int = 0
    co2_MEN: int = 0

    temperature_WOMEN: float = 0
    humidity_WOMEN: float = 0
    pm2_5_WOMEN: int = 0
    pm10_WOMEN: int = 0
    co2_WOMEN: int = 0


class AirQualityRealtimeInfoOut(Schema):
    terminal_id: str

    temperature_MEN: float = 0
    humidity_MEN: float = 0
    pm2_5_MEN: int = 0
    pm10_MEN: int = 0
    co2_MEN: int = 0
    h2s_MEN: int = 0
    nh3_MEN: int = 0

    temperature_WOMEN: float = 0
    humidity_WOMEN: float = 0
    pm2_5_WOMEN: int = 0
    pm10_WOMEN: int = 0
    co2_WOMEN: int = 0
    h2s_WOMEN: int = 0
    nh3_WOMEN: int = 0


class AirQualityWindowMean(Schema):
    terminal_id: str
    time: datetime = Field(..., alias="_time", description="采样时间")
    temperature: float = None
    humidity: float = None
    pm2_5: int = None
    pm10: int = None
    co2: int = None
    h2s: int = None
    nh3: int = None


class AirQualityWindowMeanOut(Schema):
    terminal_id: str
    toilet_name: str = None

    data: List[AirQualityWindowMean]


class BatchAirQualityWindowMean(Schema):
    terminal_id: str = None
    temperature: float = None
    humidity: float = None
    pm2_5: int = None
    pm10: int = None
    co2: int = None
    h2s: int = None
    nh3: int = None


class BatchAirQualityWindowMeanOut(BatchAirQualityWindowMean):
    toilet_name: str = None
    code: str = None
    time: datetime
