from ninja import ModelSchema
from pydantic import Field

from recycle.models import Company, CompanyManager


class CompanyManagerOut(ModelSchema):
    class Config:
        model = CompanyManager
        model_exclude = ["user"]


class CompanyOut(ModelSchema):
    manager: CompanyManagerOut
    vehicle_count: int = Field(None, title="车辆数")

    class Config:
        model = Company
        model_fields = "__all__"
