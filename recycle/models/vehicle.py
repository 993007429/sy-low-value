from django.db import models

from infra.db.models import BaseModel


class VehicleType(models.TextChoices):
    RECYCLE = "RECYCLE", "可回收物运输车"
    LARGE_RUBBISH = "LARGE_RUBBISH", "大件垃圾运输车"


class EnergyType(models.TextChoices):
    OIL = "OIL", "燃油"
    NEW_ENERGY = "NEW_ENERGY", "新能源"


class BaseVehicle(BaseModel):
    """清运公司车辆基类，车辆和车辆草稿使用相同数据库结构"""

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    plate_number = models.CharField("车牌号", max_length=32, unique=True)
    service_street = models.ForeignKey("Region", on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField("车辆类型", max_length=32, choices=VehicleType.choices)
    energy_type = models.CharField("能源类型", max_length=32, choices=EnergyType.choices)
    load = models.FloatField("载重（t）")
    meet_spec = models.BooleanField("是否按规范喷涂")

    class Meta:
        abstract = True

    @property
    def service_street_code(self):
        return self.service_street.code

    @property
    def service_street_name(self):
        return self.service_street.name

    @property
    def company_name(self):
        return self.company.name


class Vehicle(BaseVehicle):
    """清运公司车辆"""

    pass
