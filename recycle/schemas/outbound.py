from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import AnyHttpUrl, Field


class OutboundRecordBase(Schema):
    station_uuid: str = Field(title="中转站uuid", max_length=36)
    plate_number: str = Field(title="车牌号", max_length=32)

    driver: str = Field(default=None, title="司机姓名", max_length=32)
    weigher: str = Field(default=None, title="司磅员姓名", max_length=32)
    carrier_name: str = Field(default=None, title="运输单位", max_length=255)

    tare_weight: float = Field(title="皮重（kg）")
    gross_weight: float = Field(title="毛重（kg）")
    net_weight: float = Field(title="净重（kg）")
    tare_weight_time: datetime = Field(title="皮重时间")
    gross_weight_time: datetime = Field(title="毛重时间")
    net_weight_time: datetime = Field(title="净重时间")

    recyclables_type: str = Field(title="可回收物类型, e.g. 低值", max_length=32)
    category: str = Field(title="细分品类 e.g. 废塑料")

    plate_number_photo_in: AnyHttpUrl = Field(default=None, title="进入时车牌识别照片")
    vehicle_head_photo_in: AnyHttpUrl = Field(default=None, title="进入时车头照片")
    vehicle_roof_photo_in: AnyHttpUrl = Field(default=None, title="进入时车顶照片")
    plate_number_photo_out: AnyHttpUrl = Field(default=None, title="离开时车牌识别照片")
    vehicle_head_photo_out: AnyHttpUrl = Field(default=None, title="离开时车头照片")
    vehicle_roof_photo_out: AnyHttpUrl = Field(default=None, title="离开时车顶照片")

    place_to_go: str = Field(default=None, title="去向")


class OutboundRecordIn(OutboundRecordBase):
    pass


class OutboundRecordOut(OutboundRecordIn):
    station_id: str = Field(title="中转站id")
    id: str


class OutboundRecordPaginationOut(Schema):
    count: int
    total_weight: float
    results: List[OutboundRecordOut] = []
