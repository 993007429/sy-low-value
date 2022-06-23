from django.db import models

from infra.db.models import BaseModel


class Company(BaseModel):
    """清运公司"""
    name = models.CharField("公司名称", max_length=255, unique=True)
    uniform_social_credit_code = models.CharField("统一社会信用代码", max_length=32, unique=True)
    address = models.CharField("公司地址", max_length=255)
    area_code = models.CharField("注册区编码", max_length=32)
    area_name = models.CharField("注册区名称", max_length=32)
    form = models.CharField("企业类型", max_length=32)
    legal_person = models.CharField("法人", max_length=32)
    legal_person_id_card = models.CharField("法人身份证", max_length=32)
    business_license = models.CharField("营业执照", max_length=512)
    qualification = models.CharField("资质", max_length=512)
    admin = models.OneToOneField("CompanyAdmin", on_delete=models.CASCADE)
