from ninja import Schema
from pydantic import Field


class CompanyIn(Schema):
    name: str = Field(title="公司名称", max_length=255)
    uniform_social_credit_code: str = Field(title="统一社会信用代码", max_length=32)
    address: str = Field(title="公司地址", max_length=255)
    area_code: str = Field(title="注册区编码", max_length=32)
    form: str = Field(title="企业类型", max_length=32)
    legal_person: str = Field(title="法人", max_length=32)
    legal_person_id_card: str = Field(title="法人身份证", max_length=32)
    business_license: str = Field(title="营业执照", max_length=512)
    qualification: str = Field(title="资质", max_length=512)
    # admin = models.OneToOneField("CompanyAdmin", on_delete=models.CASCADE)
