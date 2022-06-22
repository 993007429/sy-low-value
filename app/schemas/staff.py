from ninja import ModelSchema, Schema
from pydantic import AnyUrl, Field, validator

from app.models.staff import GenderEnum, Staff


class StaffIn(Schema):
    name: str = Field(..., title="姓名", max_length=32)
    job_number: str = Field(None, title="工号", max_length=64)
    work_card: str = Field(None, title="工牌", max_length=64)
    gender: GenderEnum = Field(None, title="性别")
    manage_toilet_id: int = Field(None, title="管理公厕")
    organization_id: int = Field(None, title="管理单位")
    phone: str = Field(None, title="手机号")
    photo: AnyUrl = Field(None, title="照片")
    remark: str = Field(None, title="备注", max_length=255)

    @validator("job_number")
    def validate_job_number(cls, job_number, values):
        if not job_number:  # 数据库存None不存空字符串
            job_number = None
        return job_number

    @validator("work_card")
    def validate_work_card(cls, work_card, values):
        if not work_card:  # 数据库存None不存空字符串
            work_card = None
        return work_card


class StaffOut(ModelSchema):
    organization_name: str = None
    toilet_name: str = None

    class Config:
        model = Staff
        model_fields = "__all__"
