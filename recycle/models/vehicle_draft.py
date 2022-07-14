from django.db import models

from recycle.models.vehicle import BaseVehicle


class VehicleDraft(BaseVehicle):
    """清运公司车辆草稿

    草稿提交后创建审核，审核通过后保存到车辆台帐。
    """

    plate_number = models.CharField("车牌号", max_length=32)
