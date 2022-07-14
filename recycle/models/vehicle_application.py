from django.db import models

from recycle.models.vehicle import BaseVehicle
from recycle.models.vehicle_history import VehicleChangeType


class ApprovalState(models.TextChoices):
    APPROVING = "APPROVING", "审核中"
    APPROVED = "APPROVED", "审核通过"
    REJECTED = "REJECTED", "审核拒绝"


class VehicleApplication(BaseVehicle):
    """清运公司车辆注册申请"""

    plate_number = models.CharField("车牌号", max_length=32)
    # 变更类型
    change_type = models.CharField("变更类型", max_length=16, choices=VehicleChangeType.choices)
    # 审核状态
    state = models.CharField("审核状态", max_length=32, choices=ApprovalState.choices, default=ApprovalState.APPROVING)
    # 审核拒绝原因(仅在拒绝时有效)
    reason = models.CharField("审核拒绝原因", max_length=255, null=True, blank=True)
    processed_at = models.DateTimeField("审核时间", null=True, blank=True)
