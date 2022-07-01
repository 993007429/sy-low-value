from datetime import date

from ninja import Schema
from pydantic import Field


class ThroughputOut(Schema):
    throughput: float = Field(0, title="处理量")


class ThroughputByStationOut(Schema):
    station_id: str = Field(title="中转站id")
    station_name: str = Field(title="中转站名称")
    throughput: float = Field(title="处理量")
    count: int = Field(title="进场车次")


class ThroughputTrendDailyOut(Schema):
    throughput: float = Field(0, title="处理量")
    day: date


class ThroughputTrendMonthlyOut(Schema):
    throughput: float = Field(0, title="处理量")
    month: date


class ThroughputByStreetOut(Schema):
    street_name: str = Field(title="街道")
    throughput: float = Field(title="可回收物处理重量")


class ThroughputByStreetAndStationOut(Schema):
    street_name: str = Field(title="街道")
    station_name: str = Field(title="中转站名称")
    recyclables_type: str = Field(title="可回收物类型")
    throughput: float = Field(title="可回收物处理重量")
