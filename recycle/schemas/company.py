from ninja import ModelSchema

from recycle.models import Company, CompanyManager


class CompanyManagerOut(ModelSchema):
    class Config:
        model = CompanyManager
        model_exclude = ["user"]


class CompanyOut(ModelSchema):
    manager: CompanyManagerOut

    class Config:
        model = Company
        model_fields = "__all__"
