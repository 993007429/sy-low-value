from django.db import models

from infra.db.models import BaseModel


class StationNature(models.TextChoices):
    HOLD = "HOLD", "自有"
    LEASE = "LEASE", "租赁"
    ENTRUSTMENT = "ENTRUSTMENT", "委托"


class TransferStation(BaseModel):
    """可回收物中转站"""

    name = models.CharField("中转站名称", max_length=255, unique=True)
    company = models.ForeignKey(to="Company", on_delete=models.CASCADE)
    street_code = models.ForeignKey(
        to="Region", related_name="street_station", blank=True, null=True, on_delete=models.SET_NULL
    )
    comm_code = models.ForeignKey(
        to="Region", related_name="comm_station", blank=True, null=True, on_delete=models.SET_NULL
    )
    address = models.CharField("地址", max_length=255)
    longitude = models.DecimalField("经度", max_digits=20, decimal_places=11, blank=True, null=True)
    latitude = models.DecimalField("维度", max_digits=20, decimal_places=11, blank=True, null=True)
    nature = models.CharField("场所性质", max_length=32, choices=StationNature.choices)
    varieties = models.CharField("经营品种", max_length=255)
    manager_name = models.CharField("负责人姓名", max_length=32)
    manager_phone = models.CharField("负责人联系方式", max_length=32)
