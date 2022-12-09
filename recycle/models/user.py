from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from infra.db.models import BaseModel


class User(AbstractUser):
    pass


class CompanyManager(BaseModel):
    """清运公司管理员、负责人"""

    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.CharField("姓名", max_length=32)
    id_card = models.CharField("身份证", max_length=32)
    phone = models.CharField("联系电话", max_length=32)
    email = models.EmailField(unique=True)
    address = models.CharField("居住地址", max_length=255)
    id_card_front = models.CharField("身份证正面", max_length=255)
    id_card_back = models.CharField("身份证背面", max_length=255)


class PlatformManager(BaseModel):
    """再生资源平台管理员"""

    AREA = "AREA"
    STREET = "STREET"

    ROLE_CHOICES = ((AREA, "区级管理员"), (STREET, "街道管理员"))

    user = models.OneToOneField("User", on_delete=models.CASCADE)
    role = models.CharField("角色", max_length=16, choices=ROLE_CHOICES, default=AREA)
    region = models.ForeignKey(
        "Region",
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        to_field="code",
        db_column="region_code",
        default=settings.REGION_CODE,
    )


class HazardousWasteCompany(BaseModel):
    """有害垃圾清运公司"""

    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField("密码", max_length=128)
