from django.db import models

from infra.db.models import BaseModel


class AppVersion(BaseModel):
    """终端软件版本、蓝牙是否在线等"""

    terminal_id = models.CharField("终端号", max_length=64, unique=True)
    version_code = models.PositiveIntegerField()
    version_name = models.CharField(max_length=64)
    bluetooth_is_online = models.BooleanField(default=True)
