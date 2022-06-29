from datetime import datetime

from ninja import Schema
from pydantic import Field


class RecordInboundBase(Schema):
    inbound_time: datetime = Field(title="进场时间")
    station: str = Field(title="中转站名称", max_length=255)
    weighman: str = Field(title="司磅员姓名", max_length=32)
    plate_number: str = Field(title="车牌号", max_length=32)
    driver: str = Field(title="司机姓名", max_length=32)
    company: str = Field(title="运输公司名称", max_length=255)
    source_street: str = Field(title="来源街道", max_length=255)
    recyclables_type: str = Field(title="可回收物类型", max_length=32)
    net_weight: str = Field(title="净重（kg）")
    plate_number_photo: str = Field(title="车牌识别照片", max_length=255)
    car_head_photo: str = Field(title="车头照片", max_length=255)
    car_roof_photo: str = Field(title="车顶照片", max_length=255)


class RecordInboundIn(RecordInboundBase):
    pass


class RecordInboundOut(RecordInboundBase):
    pass


class RecordOutboundBase(Schema):
    inbound_time: datetime = Field(title="进场时间")
    station: str = Field(title="中转站名称", max_length=255)
    weighman: str = Field(title="司磅员姓名", max_length=32)
    plate_number: str = Field(title="车牌号", max_length=32)
    driver: str = Field(title="司机姓名", max_length=32)
    company: str = Field(title="运输公司名称", max_length=255)
    source_street: str = Field(title="来源街道", max_length=255)
    category_type: str = Field(title="细分品类", max_length=32)
    net_weight: str = Field(title="净重（kg）")
    plate_number_photo: str = Field(title="车牌识别照片", max_length=255)
    car_head_photo: str = Field(title="车头照片", max_length=255)
    car_roof_photo: str = Field(title="车顶照片", max_length=255)
    went: str = Field(title="去向", max_length=255)


class RecordOutboundIn(RecordOutboundBase):
    pass


class RecordOutboundOut(RecordOutboundBase):
    pass
