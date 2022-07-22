from ninja import ModelSchema, Schema
from pydantic import AnyHttpUrl, Field

from recycle.models import Driver


class DriverIn(Schema):
    name: str = Field(..., title="姓名", max_length=32)
    id_card: str = Field(..., title="身份证", max_length=32)
    phone: str = Field(..., title="联系电话", max_length=32)
    license_photo: AnyHttpUrl = Field(..., title="驾驶证照片")
    id_card_front: AnyHttpUrl = Field(..., title="身份证正面照片")
    id_card_back: AnyHttpUrl = Field(..., title="身份证反面照片")


class DriverOut(ModelSchema):
    class Config:
        model = Driver
        model_fields = "__all__"
