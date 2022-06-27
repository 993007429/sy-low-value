from django.db import models

from infra.db.models import BaseModel


class VehicleType(models.TextChoices):
    RECYCLE = "RECYCLE", "可回收物运输车"
    LARGE_RUBBISH = "LARGE_RUBBISH", "大件垃圾运输车"


class EnergyType(models.TextChoices):
    OIL = "OIL", "燃油"
    NEW_ENERGY = "NEW_ENERGY", "新能源"


class Vehicle(BaseModel):
    """清运公司车辆"""

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    plate_number = models.CharField("车牌号", max_length=32, unique=True)
    service_street = models.ForeignKey("Region", on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField("车辆类型", max_length=32, choices=VehicleType.choices)
    energy_type = models.CharField("能源类型", max_length=32, choices=EnergyType.choices)
    load = models.PositiveSmallIntegerField("载重（t）")
    meet_spec = models.BooleanField("是否按规范喷涂")

    @property
    def service_street_code(self):
        return self.service_street.code

    @property
    def service_street_name(self):
        return self.service_street.name
