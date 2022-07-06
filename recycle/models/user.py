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

    user = models.OneToOneField("User", on_delete=models.CASCADE)
