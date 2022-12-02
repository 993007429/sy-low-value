from django.db import models

from recycle.models.vehicle import BaseVehicle


class VehicleChangeType(models.TextChoices):
    """车辆变更类型"""

    NEW = "NEW", "新增"
    CHANGE = "CHANGE", "变更"
    DELETE = "DELETE", "删除"


class VehicleHistory(BaseVehicle):
    """清运公司车辆变更历史"""

    plate_number = models.CharField("车牌号", max_length=32)
    change_type = models.CharField("变更类型", max_length=16, choices=VehicleChangeType.choices)
