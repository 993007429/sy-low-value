from django.db import models

from infra.db.models import BaseModel


class RegionGrade(models.IntegerChoices):
    CITY = 1
    AREA = 2
    STREET = 3
    COMMUNITY = 4


class Region(BaseModel):
    code = models.CharField("编码", max_length=32, unique=True)
    name = models.CharField("区域名", max_length=64)
    grade = models.PositiveSmallIntegerField("区域级别", choices=RegionGrade.choices)
    rank = models.SmallIntegerField("排序", default=0)
    parent = models.ForeignKey("Region", on_delete=models.CASCADE, null=True, blank=True)
