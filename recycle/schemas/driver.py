from datetime import date

from ninja import Schema, ModelSchema
from pydantic import Field, AnyHttpUrl

from recycle.models import Driver


class DriverIn(Schema):
    name: str = Field(..., title="姓名", max_length=32)
    id_card: str = Field(..., title="身份证", max_length=32)
    phone: str = Field(..., title="联系电话", max_length=32)
    working_years: int = Field(..., title="从业年限", ge=0, le=100)
    joined_at: date = Field(..., title="入职日期")
    license_photo: AnyHttpUrl = Field(..., title="驾驶证照片")


class DriverOut(ModelSchema):
    class Config:
        model = Driver
        model_fields = "__all__"
