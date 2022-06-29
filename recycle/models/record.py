from django.db import models

from infra.db.models import BaseModel


class RecordInbound(BaseModel):
    """中转站进场记录"""

    inbound_time = models.DateTimeField("进场时间")
    station = models.CharField("中转站名称", max_length=255)
    weighman = models.CharField("司磅员姓名", max_length=32)
    plate_number = models.CharField("车牌号", max_length=32)
    driver = models.CharField("司机姓名", max_length=32)
    company = models.CharField("运输公司", max_length=255)
    source_street = models.CharField("来源街道", max_length=255)
    recyclables_type = models.CharField("可回收物类型", max_length=32)
    net_weight = models.FloatField("净重（kg）")
    plate_number_photo = models.CharField("车牌识别照片", max_length=255)
    car_head_photo = models.CharField("车头照片", max_length=255)
    car_roof_photo = models.CharField("车顶照片", max_length=255)


class RecordOutbound(BaseModel):
    """中转站出场记录"""

    inbound_time = models.DateTimeField("出场时间")
    station = models.CharField("中转站名称", max_length=255)
    weighman = models.CharField("司磅员姓名", max_length=32)
    plate_number = models.CharField("车牌号", max_length=32)
    driver = models.CharField("司机姓名", max_length=32)
    company = models.CharField("运输公司名称", max_length=255)
    source_street = models.CharField("来源街道", max_length=255)
    category_type = models.CharField("细分品类", max_length=32)
    net_weight = models.FloatField("净重（kg）")
    plate_number_photo = models.CharField("车牌识别照片", max_length=255)
    car_head_photo = models.CharField("车头照片", max_length=255)
    car_roof_photo = models.CharField("车顶照片", max_length=255)
    went = models.CharField("去向", max_length=255)
