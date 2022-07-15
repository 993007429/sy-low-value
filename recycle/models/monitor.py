from django.db import models

from infra.db.models import BaseModel


class Monitor(BaseModel):
    """设施监控"""

    station = models.ForeignKey("TransferStation", on_delete=models.CASCADE)
    serial = models.CharField("国标编号", max_length=64)
    code = models.CharField("视频通道编号", max_length=64)
    site_type = models.CharField("位置类型", max_length=32)
    site_name = models.CharField("位置名称", max_length=32)
