from django.db import models

from infra.db.models import BaseModel


class HighValueReport(BaseModel):
    """高值填报记录"""

    street = models.ForeignKey("Region", on_delete=models.CASCADE, db_constraint=False)
    report_date = models.DateField("填报日期")
    high_value_weight = models.FloatField("高值重量（单位kg）")
    low_value_weight = models.FloatField("低值重量（单位kg）")
    reporter = models.CharField("填报人", max_length=64)
    approver = models.CharField("审核人", max_length=64)

    @property
    def street_code(self):
        return self.street.code

    @property
    def street_name(self):
        return self.street.name

    class Meta:
        unique_together = ("street", "report_date")
