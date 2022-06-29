from django.contrib.postgres.fields import ArrayField
from django.db import models

from infra.db.models import BaseModel


class StationNature(models.TextChoices):
    HOLD = "HOLD", "自有"
    LEASE = "LEASE", "租赁"
    ENTRUSTMENT = "ENTRUSTMENT", "委托"


class RubbishVariety(models.TextChoices):
    """经营品种"""

    PAPER = "PAPER", "废纸"
    METAL = "METAL", "废金属"
    PLASTIC = "PLASTIC", "废塑料"
    GLASS = "GLASS", "废玻璃"
    FABRIC = "FABRIC", "废织物"
    ELECTRONICS = "ELECTRONICS", "废弃电器电子产品"
    LARGE_FURNITURE = "LARGE_FURNITURE", "废弃大件家具"


class TransferStation(BaseModel):
    """可回收物中转站"""

    name = models.CharField("中转站名称", max_length=255, unique=True)
    street = models.ForeignKey(
        to="Region",
        db_constraint=False,
        related_name="street_stations",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    community = models.ForeignKey(
        to="Region",
        db_constraint=False,
        related_name="community_stations",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    management_company = models.CharField("管理单位", max_length=255)
    address = models.CharField("地址", max_length=255)
    longitude = models.DecimalField("经度", max_digits=20, decimal_places=11)
    latitude = models.DecimalField("维度", max_digits=20, decimal_places=11)
    nature = models.CharField("场所性质", max_length=32, choices=StationNature.choices)
    varieties = ArrayField(
        base_field=models.CharField(max_length=32, choices=RubbishVariety.choices),
        verbose_name="经营品种",
        default=list,
        blank=True,
    )
    manager_name = models.CharField("负责人姓名", max_length=32)
    manager_phone = models.CharField("负责人联系方式", max_length=32)
