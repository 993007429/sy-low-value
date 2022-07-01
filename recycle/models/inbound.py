from django.db import models

from infra.db.models import BaseModel


class InboundRecord(BaseModel):
    """中转站进场记录, 即把可回收物送到可回收物中转站"""

    station = models.ForeignKey("TransferStation", on_delete=models.CASCADE)
    uuid = models.CharField(unique=True, max_length=36)
    plate_number = models.CharField("车牌号", max_length=32)
    driver = models.CharField("司机姓名", max_length=32, null=True, blank=True)
    weigher = models.CharField("司磅员姓名", max_length=32, null=True, blank=True)
    carrier = models.ForeignKey("Company", verbose_name="清运公司", on_delete=models.SET_NULL, null=True)
    carrier_name = models.CharField("运输单位", max_length=255, null=True, blank=True)
    source_street_name = models.CharField("来源街道", max_length=255, null=True, blank=True)

    tare_weight = models.FloatField("皮重（kg）")
    gross_weight = models.FloatField("毛重（kg）")
    net_weight = models.FloatField("净重（kg）")
    tare_weight_time = models.DateTimeField("皮重时间")
    gross_weight_time = models.DateTimeField("毛重时间")
    net_weight_time = models.DateTimeField("净重时间")

    recyclables_type = models.CharField("可回收物类型", max_length=32)

    plate_number_photo_in = models.CharField("进场车牌识别照片", max_length=512, null=True, blank=True)
    vehicle_head_photo_in = models.CharField("进场车头照片", max_length=512, null=True, blank=True)
    vehicle_roof_photo_in = models.CharField("进场车顶照片", max_length=512, null=True, blank=True)

    plate_number_photo_out = models.CharField("出场车牌识别照片", max_length=512, null=True, blank=True)
    vehicle_head_photo_out = models.CharField("出场车头照片", max_length=512, null=True, blank=True)
    vehicle_roof_photo_out = models.CharField("出场车顶照片", max_length=512, null=True, blank=True)

    @property
    def station_name(self):
        return self.station.name
