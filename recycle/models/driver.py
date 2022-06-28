from django.db import models

from infra.db.models import BaseModel


class Driver(BaseModel):
    """清运公司司机"""

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    name = models.CharField("姓名", max_length=32)
    id_card = models.CharField("身份证", max_length=32)
    phone = models.CharField("联系电话", max_length=32)
    working_years = models.PositiveSmallIntegerField("从业年限")
    joined_at = models.DateField("入职日期")
    license_photo = models.CharField("驾驶证照片", max_length=255)

    class Meta:
        unique_together = (
            ("company", "id_card"),
            ("company", "phone"),
        )
