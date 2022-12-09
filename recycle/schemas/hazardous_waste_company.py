from ninja import ModelSchema, Schema
from pydantic import Field

from recycle.models import HazardousWasteCompany


class HazardousWasteCompanyIn(Schema):
    username: str = Field(..., title="用户名")
    password: str = Field(..., title="密码", min_length=6, max_length=32)
    name: str = Field(..., title="公司名称")


class HazardousWasteCompanyOut(ModelSchema):
    username: str = Field(..., alias="user.username")

    class Config:
        model = HazardousWasteCompany
        model_exclude = ["user"]
