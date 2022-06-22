from django.db import models

from infra.db.models import BaseModel


class ToiletType(BaseModel):
    """公厕类型"""

    name = models.CharField(max_length=128, unique=True)
