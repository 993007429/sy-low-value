import re
from typing import Literal

from ninja import Schema
from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, validator

from recycle.models import CompanyForm
from recycle.models.company_application import ApprovalState


class CompanyApplicationBase(Schema):
    """公司注册表单"""

    # 公司信息
    name: str = Field(title="公司名称", max_length=255)
    uniform_social_credit_code: str = Field(title="统一社会信用代码", max_length=18)
    address: str = Field(title="公司地址", max_length=255)
    registration_region_code: str = Field(title="注册区编码", max_length=32)
    form: CompanyForm = Field(title="企业类型")
    legal_person: str = Field(title="法人", max_length=32)
    legal_person_id_card: str = Field(title="法人身份证", max_length=32)
    business_license: AnyHttpUrl = Field(title="营业执照")
    qualification: AnyHttpUrl = Field(title="资质")
    # 负责人信息
    manager_name: str = Field(title="姓名", max_length=32)
    manager_id_card: str = Field(title="身份证", max_length=32)
    manager_phone: str = Field(title="联系电话", max_length=32)
    manager_email: EmailStr = Field(title="邮箱")
    manager_address: str = Field(title="居住地址", max_length=255)
    manager_id_card_front: AnyHttpUrl = Field(title="身份证正面")
    manager_id_card_back: AnyHttpUrl = Field(title="身份证背面")

    @validator("uniform_social_credit_code")
    def validate_uniform_social_credit_code(cls, v):
        if not re.fullmatch(r"^\w{18}$", v):
            raise ValueError("非法的统一社会信用代码")
        return v


class CompanyApplicationIn(CompanyApplicationBase):
    pass


class CompanyApplicationOut(CompanyApplicationBase):
    registration_region_name: str = Field(title="注册区名称", max_length=32)
    state: ApprovalState = Field(None, title="审核状态")
    reason: str = Field(None, title="审核拒绝原因")
    id: int


class CompanyApplicationOperationIn(BaseModel):
    state: Literal[ApprovalState.APPROVED, ApprovalState.REJECTED] = Field(..., title="审核状态")
    reason: str = Field(None, title="审核拒绝原因")

    @validator("reason")
    def validate_reason(cls, reason, values):
        if values["state"] == ApprovalState.REJECTED and not reason:
            raise ValueError("reason must not be empty when state is REJECTED")
        return reason
