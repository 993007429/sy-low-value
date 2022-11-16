from django.db import models

from infra.db.models import BaseModel


class StandingBookManager(models.Manager):
    """台帐车辆入场记录"""

    def get_queryset(self):
        return super().get_queryset().filter(carrier__isnull=False)


class InboundRecord(BaseModel):
    """中转站进场记录, 即把可回收物送到可回收物中转站。目前非系统台帐车辆也允许录入"""

    station = models.ForeignKey("TransferStation", on_delete=models.CASCADE)
    uuid = models.CharField(unique=True, max_length=36)
    plate_number = models.CharField("车牌号", max_length=32)
    driver = models.CharField("司机姓名", max_length=32, null=True, blank=True)
    weigher = models.CharField("司磅员姓名", max_length=32, null=True, blank=True)
    carrier = models.ForeignKey("Company", verbose_name="清运公司", on_delete=models.SET_NULL, null=True)
    source_street = models.ForeignKey("Region", on_delete=models.RESTRICT, null=True, blank=True)

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

    objects = models.Manager()  # The default manager.
    standing_book = StandingBookManager()

    @property
    def station_name(self):
        return self.station.name

    @property
    def source_street_name(self):
        return self.source_street.name if self.source_street else None

    @property
    def source_street_code(self):
        return self.source_street.code if self.source_street else None

    @property
    def carrier_name(self):
        return self.carrier.name if self.carrier else None
