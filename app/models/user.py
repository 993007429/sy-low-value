from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=32)
    phone = models.CharField(max_length=32, null=True)
    id_card = models.CharField("身份证", max_length=32, null=True)
    roles = models.ManyToManyField("Role")
    organization = models.ForeignKey("Organization", db_constraint=False, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-pk"]


class WeChatGenderEnum(IntEnum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class WeChatUser(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, db_constraint=False)
    openid = models.CharField(max_length=255)
    nickname = models.CharField(max_length=100, null=True)
    avatar = models.CharField(max_length=255, null=True)
    unionid = models.CharField(max_length=100, null=True)
    gender = models.IntegerField(WeChatGenderEnum, default=WeChatGenderEnum.UNKNOWN)
    city = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    session_key = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nickname or self.user.username
