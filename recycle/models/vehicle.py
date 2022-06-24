from django.db import models

from infra.db.models import BaseModel


class Vehicle(BaseModel):
    """清运公司车辆"""

    class VehicleType(models.TextChoices):
        RECYCLE = "RECYCLE", "可回收物运输车"
        LARGE_RUBBISH = "LARGE_RUBBISH", "大件垃圾运输车"

    class EnergyType(models.TextChoices):
        OIL = "OIL", "燃油"
        NEW_ENERGY = "NEW_ENERGY", "新能源"

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    plate_number = models.CharField("车牌号", max_length=32)
    street_code = models.CharField("服务街道编码", max_length=32)
    street_name = models.CharField("服务街道名称", max_length=32)
    type = models.CharField("车辆类型", max_length=32, choices=VehicleType.choices)
    energy_type = models.CharField("能源类型", max_length=32, choices=EnergyType.choices)
    load = models.PositiveSmallIntegerField("载重（t）")
    meet_specification = models.BooleanField("是否按规范喷涂")
