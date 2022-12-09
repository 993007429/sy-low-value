from django.db import models

from infra.db.models import BaseModel


class HazardousWasteReport(BaseModel):
    """有害垃圾填报记录"""

    company = models.ForeignKey("HazardousWasteCompany", on_delete=models.CASCADE, db_constraint=False)
    report_date = models.DateField("填报日期")
    weight = models.FloatField("高值重量（单位kg）")
    approver = models.CharField("审核人", max_length=64)

    @property
    def company_name(self):
        return self.company.name

    class Meta:
        unique_together = ("company", "report_date")
