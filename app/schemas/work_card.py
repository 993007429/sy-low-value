from datetime import datetime

from ninja import Schema
from pydantic import Field


class WorkCardIn(Schema):
    terminal_id: str
    sensor_id: str
    gather_time: datetime
    work_card: str = Field(..., description="工牌号")


class WorkCardOut(Schema):
    timestamp: datetime
