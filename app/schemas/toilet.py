from datetime import date
from typing import List

from ninja import ModelSchema, Schema
from pydantic import Field, validator

from app.models.sensors import InstallationLocation, SensorType
from app.models.toilet import FlushType, PositionEnum, StatusEnum, SupportingFacilityEnum, Toilet


class SensorIn(Schema):
    sensor_id: str = Field(..., title="传感器编号")
    sensor_type: SensorType = Field(..., title="传感器类型")
    installation_location: InstallationLocation = Field(..., title="安装位置")
    serial: int = Field(None, title="厕位序号")

    @validator("serial")
    def serial_required(cls, serial, values, **kwargs):
        sensor_type = values.get("sensor_type")
        if sensor_type != SensorType.TOILET_SEAT:  # 只有是坑位传感器，坑位序号才有用
            return None
        elif not serial:
            raise ValueError("serial is required when sensor_type is TOILET_SEAT")
        else:
            return serial


class SensorUpdate(SensorIn):
    id: int = None


class SensorOut(Schema):
    id: int
    sensor_id: str = Field(..., title="传感器编号")
    sensor_type: str = Field(..., title="传感器类型")
    installation_location: str = Field(..., title="安装位置")
    serial: int = Field(None, title="厕位序号")


class ToiletIn(Schema):
    name: str = Field(max_length=128, title="公厕名称")
    management_id: int = Field(title="管理单位")
    toilet_type_id: int = Field(title="公厕类型")
    terminal_id: str = Field(..., title="终端号")
    code: str = Field(default=None, title="编号")
    flush_type: FlushType = Field(default=None, title="冲洗方式")
    road: str = Field(None, title="路段名称")
    area: float = Field(None, title="占地面积")
    built_at: date = Field(None, title="建更时间")
    men_toilet_nums: int = Field(None, title="男厕位数")
    women_toilet_nums: int = Field(None, title="女厕位数")
    genderless_toilet_nums: int = Field(None, title="无性别厕位数")
    position_type: PositionEnum = Field(None, title="移动/固定")
    status: StatusEnum = Field(StatusEnum.NORMAL, title="当前状态")
    manager_id: int = Field(None, title="负责人id")
    latitude: float = Field(None, title="纬度")
    longitude: float = Field(None, title="经度")
    address: str = Field(None, title="地址")
    remark: str = None
    photos: List[str]
    supporting_facilities: List[SupportingFacilityEnum] = Field(None, title="配套开关")

    sensors: List[SensorIn] = Field(default_factory=list, title="传感器")


class ToiletUpdate(ToiletIn):
    sensors: List[SensorUpdate] = Field(default_factory=list, title="传感器")


class ToiletOut(ModelSchema):
    management_id: int = Field(None, title="管理单位")
    management_name: str = None
    manager_id: int = Field(None, title="负责人id")
    manager_name: str = None
    toilet_type_id: int = Field(None, title="公厕类型")
    toilet_type_name: str = Field(None, title="公厕类型名称")
    photos: List[str] = []
    supporting_facilities: List[str] = []
    sensors: List[SensorOut] = []
    distance: float = Field(None, title="距离")

    class Config:
        model = Toilet
        model_fields = [
            "id",
            "name",
            "code",
            "terminal_id",
            "flush_type",
            "road",
            "area",
            "built_at",
            "men_toilet_nums",
            "women_toilet_nums",
            "genderless_toilet_nums",
            "position_type",
            "status",
            "longitude",
            "latitude",
            "address",
            "remark",
            "camera_serial",
            "camera_channel",
        ]


class ToiletRealtimeInfoOut(Schema):
    """公厕传感器实时数据"""

    id: int
    terminal_id: str
    name: str
    code: str = None
    address: str = None
    supporting_facilities: List[str]
    photos: List[str]
    camera_serial: str = None
    camera_channel: str = None

    temperature_MEN: float = 0
    humidity_MEN: float = 0
    pm2_5_MEN: int = 0
    pm10_MEN: int = 0
    co2_MEN: int = 0
    h2s_MEN: int = 0
    nh3_MEN: int = 0

    temperature_WOMEN: float = 0
    humidity_WOMEN: float = 0
    pm2_5_WOMEN: int = 0
    pm10_WOMEN: int = 0
    co2_WOMEN: int = 0
    h2s_WOMEN: int = 0
    nh3_WOMEN: int = 0

    passenger_volume: int = 0

    MEN_toilet_occupied: int = Field(0, description="男厕所坑位占用数")
    WOMEN_toilet_occupied: int = Field(0, description="女厕所坑位占用数")
    GENDERLESS_toilet_occupied: int = Field(0, description="无差别卫生间坑位占用数")
    men_toilet_total: int = Field(0, description="男厕所坑位数")
    women_toilet_total: int = Field(0, description="女厕所坑位数")
    genderless_toilet_total: int = Field(0, description="无差别卫生间坑位数")

    kwh: float = Field(0, description="电表数")
    water_meter: float = Field(0, alias="volume", description="水表数")
