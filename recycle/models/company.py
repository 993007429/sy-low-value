from enum import Enum

from django.db import models

from infra.db.models import BaseModel


class CompanyForm(str, Enum):
    """企业类型"""

    PERSONAL = "PERSONAL"  # "个人独资企业"
    PARTNERSHIP = "PARTNERSHIP"  # "合伙企业"
    JOINT_STOCK = "JOINT-STOCK"  # "股份有限公司"
    LIMITED = "LIMITED"  # "有限责任公司"

    @classmethod
    def choices(cls):
        return [(e, e.value) for e in cls]


class Company(BaseModel):
    """清运公司"""

    name = models.CharField("公司名称", max_length=255, unique=True)
    uniform_social_credit_code = models.CharField("统一社会信用代码", max_length=32, unique=True)
    address = models.CharField("公司地址", max_length=255)
    area_code = models.CharField("注册区编码", max_length=32)
    area_name = models.CharField("注册区名称", max_length=32)
    form = models.CharField("企业类型", choices=CompanyForm.choices(), max_length=32)
    legal_person = models.CharField("法人", max_length=32)
    legal_person_id_card = models.CharField("法人身份证", max_length=32)
    business_license = models.CharField("营业执照", max_length=512)
    qualification = models.CharField("资质", max_length=512)
    manager = models.OneToOneField("CompanyManager", on_delete=models.CASCADE)
