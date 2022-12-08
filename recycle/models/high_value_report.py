from django.db import models

from infra.db.models import BaseModel


class HighValueReport(BaseModel):
    """高值填报记录"""

    street = models.ForeignKey("Region", on_delete=models.CASCADE, db_constraint=False)
    report_date = models.DateField("填报日期")
    high_value_weight = models.FloatField("高值重量（单位吨）")
    low_value_weight = models.FloatField("低值重量（单位吨）")
    reporter = models.CharField("填报人", max_length=64)
    approver = models.CharField("审核人", max_length=64)

    class Meta:
        unique_together = ("street", "report_date")
