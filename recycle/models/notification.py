from django.db import models

from infra.db.models import BaseModel


class ServiceStreetModification(BaseModel):
    """服务街道变更"""

    plate_number = models.CharField("车牌号", max_length=32)
    source_street = models.ForeignKey(
        "Region", related_name="source_service_street_modifications", db_constraint=False, on_delete=models.CASCADE
    )
    target_street = models.ForeignKey(
        "Region", related_name="target_service_street_modifications", db_constraint=False, on_delete=models.CASCADE
    )
    read = models.BooleanField("已读", default=False)

    class Meta:
        ordering = ["-id"]

    @property
    def source_street_name(self):
        return self.source_street.name

    @property
    def target_street_name(self):
        return self.target_street.name
