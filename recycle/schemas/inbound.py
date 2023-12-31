from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import AnyHttpUrl, Field


class InboundRecordBase(Schema):
    plate_number: str = Field(title="车牌号", max_length=32)
    uuid: str = Field(title="记录唯一id", max_length=36, min_length=32)

    driver: str = Field(default=None, title="司机姓名", max_length=32)
    weigher: str = Field(default=None, title="司磅员姓名", max_length=32)

    tare_weight: float = Field(title="皮重（kg）")
    gross_weight: float = Field(title="毛重（kg）")
    net_weight: float = Field(title="净重（kg）")
    tare_weight_time: datetime = Field(title="皮重时间")
    gross_weight_time: datetime = Field(title="毛重时间")
    net_weight_time: datetime = Field(title="净重时间")

    recyclables_type: str = Field(title="可回收物类型, e.g. 低值", max_length=32)

    plate_number_photo_in: AnyHttpUrl = Field(default=None, title="车牌识别照片")
    vehicle_head_photo_in: AnyHttpUrl = Field(default=None, title="车头照片")
    vehicle_roof_photo_in: AnyHttpUrl = Field(default=None, title="车顶照片")
    plate_number_photo_out: AnyHttpUrl = Field(default=None, title="出场车牌识别照片")
    vehicle_head_photo_out: AnyHttpUrl = Field(default=None, title="出场车头照片")
    vehicle_roof_photo_out: AnyHttpUrl = Field(default=None, title="出场车顶照片")


class InboundRecordIn(InboundRecordBase):
    station_uuid: str = Field(title="中转站uuid", max_length=255)


class InboundRecordOut(InboundRecordBase):
    station_id: str = Field(title="中转站id")
    station_name: str = Field(default=None, title="中转站名称")
    source_street_name: str = Field(default=None, title="来源街道")
    source_street_code: str = Field(default=None, title="来源街道")
    carrier_id: str = Field(None, title="运输单位（清运公司）id")
    carrier_name: str = Field(default=None, title="运输单位")
    id: str


class InboundRecordPaginationOut(Schema):
    count: int
    total_weight: float
    results: List[InboundRecordOut] = []
