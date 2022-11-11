from ninja import Schema
from pydantic import Field


class ServiceStreetModificationOut(Schema):
    plate_number: str = Field(..., title="车牌号")
    source_street_id: str = Field(..., title="原服务街道id")
    source_street_name: str = Field(..., title="原服务街道名")
    target_street_id: str = Field(..., title="现服务街道id")
    target_street_name: str = Field(..., title="现服务街道名")
