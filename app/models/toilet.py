from django.contrib.postgres.fields import ArrayField
from django.db import models

from infra.db.models import BaseModel


class FlushType(models.TextChoices):
    """冲洗方式"""

    BUBBLE = "BUBBLE", "发泡"
    WATER = "WATER", "冲水"
    DRY = "DRY", "旱厕"
    WATER_VAPOR = "WATER_VAPOR", "水汽一体"
    OTHER = "OTHER", "其他"


class PositionEnum(models.TextChoices):
    """公厕固定、可移动"""

    FIXED = "FIXED", "固定"
    MOVABLE = "MOVABLE", "移动"


class StatusEnum(models.TextChoices):
    """公厕状态"""

    NORMAL = "NORMAL", "正常"
    OUT_OF_SERVICE = "OUT_OF_SERVICE", "停用"
    MAINTAIN = "MAINTAIN", "维修"


class SupportingFacilityEnum(models.TextChoices):
    """公厕配套设施"""

    PAPER = "PAPER", "厕纸"
    HAND_SANITIZER = "HAND_SANITIZER", "洗手液"
    NURSING_ROOM = "NURSING_ROOM", "母婴室"
    GENDERLESS_ROOM = "GENDERLESS_ROOM", "第三性别卫生间"
    WIFI = "WIFI", "wifi"
    AMMETER = "AMMETER", "电表"
    WATER_METER = "WATER_METER", "水表"
    H2S = "H2S", "硫化氢"
    OUT_OF_SERVICE = "OUT_OF_SERVICE", "停用"
    PAY = "PAY", "收费"


class Toilet(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    management = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    toilet_type = models.ForeignKey(
        "ToiletType",
        on_delete=models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    code = models.CharField("编号", max_length=64, unique=True, null=True, blank=True)
    terminal_id = models.CharField("终端号", max_length=64, unique=True)
    flush_type = models.CharField("冲洗方式", max_length=32, choices=FlushType.choices, null=True, blank=True)
    road = models.CharField("路段名称", max_length=128, null=True, blank=True)
    area = models.FloatField("占地面积", null=True, blank=True)
    built_at = models.DateField("建造时间", null=True, blank=True)
    men_toilet_nums = models.PositiveSmallIntegerField("男厕位", null=True, blank=True)
    women_toilet_nums = models.PositiveSmallIntegerField("女厕位", null=True, blank=True)
    genderless_toilet_nums = models.PositiveSmallIntegerField("无性别厕位", null=True, blank=True)
    position_type = models.CharField("", max_length=32, choices=PositionEnum.choices, null=True, blank=True)
    status = models.CharField("当前状态", max_length=32, choices=StatusEnum.choices, default=StatusEnum.NORMAL)
    manager = models.ForeignKey("Staff", on_delete=models.SET_NULL, db_constraint=False, null=True, blank=True)

    longitude = models.FloatField("经度", null=True, blank=True)
    latitude = models.FloatField("纬度", null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    photos = ArrayField(models.TextField())
    supporting_facilities = ArrayField(models.CharField(max_length=32, choices=SupportingFacilityEnum.choices))

    # 视频监控
    camera_serial = models.CharField("摄像机国标编号", max_length=64, null=True)
    camera_channel = models.CharField("通道", max_length=64, null=True)

    @property
    def sensors(self):
        return self.sensor_set.all()

    @property
    def management_name(self):
        return self.management.name if self.management else None

    @property
    def toilet_type_name(self):
        return self.toilet_type.name if self.toilet_type else None

    @property
    def manager_name(self):
        return self.manager.name if self.manager else None
