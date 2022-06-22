from django.db import models

from infra.db.models import BaseModel


class GenderEnum(models.TextChoices):
    MALE = "M", "男"
    FEMALE = "F", "女"


class Staff(BaseModel):
    name = models.CharField(max_length=32)
    job_number = models.CharField("工号", max_length=64, unique=True, null=True, blank=True)
    work_card = models.CharField("工牌", max_length=64, unique=True, null=True, blank=True)
    gender = models.CharField("性别", max_length=16, choices=GenderEnum.choices, null=True, blank=True)
    manage_toilet = models.ForeignKey("Toilet", db_constraint=False, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(
        "Organization", on_delete=models.DO_NOTHING, db_constraint=False, null=True, blank=True
    )
    phone = models.CharField(max_length=32, null=True, blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)

    @property
    def organization_name(self):
        return self.organization.name if self.organization else None

    @property
    def toilet_name(self):
        return self.manage_toilet.name if self.manage_toilet else None
