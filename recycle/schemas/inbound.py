from datetime import datetime

from ninja import Schema
from pydantic import AnyHttpUrl, Field


class InboundRecordBase(Schema):
    station_name: str = Field(title="中转站名称", max_length=255)
    plate_number: str = Field(title="车牌号", max_length=32)
    driver: str = Field(title="司机姓名", max_length=32)
    weigher: str = Field(title="司磅员姓名", max_length=32)
    carrier_name: str = Field(title="运输单位", max_length=255)

    tare_weight: float = Field(title="皮重（kg）")
    gross_weight: float = Field(title="毛重（kg）")
    net_weight: float = Field(title="净重（kg）")
    tare_weight_time: datetime = Field(title="皮重时间")
    gross_weight_time: datetime = Field(title="毛重时间")
    net_weight_time: datetime = Field(title="净重时间")

    recyclables_type: str = Field(title="可回收物类型, e.g. 低值", max_length=32)

    plate_number_photo_in: AnyHttpUrl = Field(title="车牌识别照片")
    vehicle_head_photo_in: AnyHttpUrl = Field(title="车头照片")
    vehicle_roof_photo_in: AnyHttpUrl = Field(title="车顶照片")
    plate_number_photo_out: AnyHttpUrl = Field(title="车牌识别照片")
    vehicle_head_photo_out: AnyHttpUrl = Field(title="车头照片")
    vehicle_roof_photo_out: AnyHttpUrl = Field(title="车顶照片")


class InboundRecordIn(InboundRecordBase):
    source_street_name: str = Field(title="来源街道", max_length=255)


class InboundRecordOut(InboundRecordIn):
    station_id: str = Field(title="中转站id")
    carrier_id: str = Field(title="运输单位（清运公司）id")
    id: str
