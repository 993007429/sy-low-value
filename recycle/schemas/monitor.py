from ninja import Schema
from pydantic import Field


class MonitorOut(Schema):
    serial: str = Field(..., title="国标编号", max_length=64)
    code: str = Field(..., title="视频通道编号", max_length=64)
    station_name: str = Field(..., title="中转站名称", alias="station.name")
    station_street_name: str = Field(..., title="中转站所属街道名称", alias="station.street.name")
    station_community_name: str = Field(..., title="中转站所属社区名称", alias="station.community.name")
    station_nature: str = Field(..., title="中转站场所性质", alias="station.nature")
    manager_name: str = Field(..., title="负责人姓名", alias="station.manager_name")
    manager_phone: str = Field(..., title="负责人联系方式", alias="station.manager_phone")
