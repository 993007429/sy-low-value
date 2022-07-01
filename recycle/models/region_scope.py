from django.db import models

from infra.db.models import BaseModel


class RegionScope(BaseModel):
    """地区范围"""

    code = models.BigIntegerField(null=True, blank=True, verbose_name=("地区编码"))
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=("地区名称"))
    lon_lat = models.TextField(blank=True, verbose_name=("经纬度"))
    lat_center = models.DecimalField(max_digits=20, decimal_places=11, blank=True, null=True)
    lon_center = models.DecimalField(max_digits=20, decimal_places=11, blank=True, null=True)
    is_null = models.IntegerField(blank=True, null=True, default=0)
