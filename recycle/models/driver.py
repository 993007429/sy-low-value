from django.db import models

from infra.db.models import BaseModel


class Driver(BaseModel):
    """清运公司司机"""

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    name = models.CharField("姓名", max_length=32)
    id_card = models.CharField("身份证", max_length=32)
    phone = models.CharField("联系电话", max_length=32)
    license_photo = models.TextField("驾驶证照片")
    id_card_front = models.TextField("身份证正面", null=True)
    id_card_back = models.TextField("身份证反面", null=True)

    class Meta:
        unique_together = (
            ("company", "id_card"),
            ("company", "phone"),
        )
