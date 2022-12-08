from datetime import date

from ninja import ModelSchema, Schema
from pydantic import Field

from recycle.models import HighValueReport
from recycle.schemas.region import RegionOut


class HighValueReportIn(Schema):
    report_date: date = Field(..., title="填报日期")
    high_value_weight: float = Field(..., title="高值重量（单位吨）")
    low_value_weight: float = Field(..., title="低值重量（单位吨）")
    reporter: str = Field(..., title="填报人", max_length=64)
    approver: str = Field(..., title="审核人", max_length=64)


class HighValueReportOut(ModelSchema):
    street: RegionOut

    class Config:
        model = HighValueReport
        model_fields = "__all__"
