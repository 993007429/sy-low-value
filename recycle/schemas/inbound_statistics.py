from ninja import Schema
from pydantic import Field


class ThroughputOut(Schema):
    throughput: float = Field(0, title="处理量")


class ThroughputByStationOut(Schema):
    station_id: str = Field(title="中转站id")
    station_name: str = Field(title="中转站名称")
    throughput: float = Field(title="处理量")
    count: int = Field(title="进场车次")
