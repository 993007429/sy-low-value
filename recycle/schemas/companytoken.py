from ninja import Schema
from pydantic import Field


class Login(Schema):
    username: str
    password: str


class CompanyToken(Schema):
    username: str
    name: str
    token: str
    user_id: int
    social_credit_code: str = Field(None, title="统一社会信用代码")
    has_transfer_station: bool = Field(False, title="运输公司是否有中转站")


class PlatformToken(Schema):
    username: str
    name: str
    token: str
    user_id: int
    role: str
