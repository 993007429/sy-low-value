from django.db import models

from infra.db.models import BaseModel


class EventType(models.TextChoices):
    OVERLOAD = "OVERLOAD", "超载"
    SPEEDING = "SPEEDING", "超速"
    OVERTIME = "OVERTIME", "超时"  # 原地停留超过一小时


class Event(BaseModel):
    """实时预警事件"""

    plate_number = models.CharField("车牌号", max_length=32)
    started_at = models.DateTimeField("事件开始时间")
    ended_at = models.DateTimeField("事件结束时间", null=True, blank=True)
    type = models.CharField("事件类型", max_length=16, choices=EventType.choices)

    class Meta:
        ordering = ["-started_at", "-id"]
