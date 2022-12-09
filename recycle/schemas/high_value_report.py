from datetime import date

from ninja import ModelSchema, Schema
from pydantic import Field

from recycle.models import HighValueReport
from recycle.schemas.region import RegionOut


class HighValueReportIn(Schema):
    report_date: date = Field(..., title="填报日期")
    high_value_weight: float = Field(..., title="高值重量（单位kg）")
    low_value_weight: float = Field(..., title="低值重量（单位kg）")
    reporter: str = Field(..., title="填报人", max_length=64)
    approver: str = Field(..., title="审核人", max_length=64)


class HighValueReportOut(ModelSchema):
    street: RegionOut

    class Config:
        model = HighValueReport
        model_fields = "__all__"


class ThroughputByStreetOut(Schema):
    street_code: str = Field(..., title="街道编码")
    street_name: str = Field(..., title="街道名称")
    throughput: float = Field(..., title="垃圾重量")
