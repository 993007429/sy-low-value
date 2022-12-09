from datetime import date

from ninja import ModelSchema, Schema
from pydantic import Field

from recycle.models.hazardous_waste_report import HazardousWasteReport


class HazardousWasteReportIn(Schema):
    report_date: date = Field(..., title="填报日期")
    weight: float = Field(..., title="重量（单位kg）")
    approver: str = Field(..., title="审核人", max_length=64)


class HazardousWasteReportOut(ModelSchema):
    company_name: str

    class Config:
        model = HazardousWasteReport
        model_fields = "__all__"


class ThroughputByCompanyOut(Schema):
    company_id: int
    company_name: str
    throughput: float = Field(0, title="有害垃圾总重量")
