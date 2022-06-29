from ninja import Schema
from pydantic import Field

from recycle.models.transfer_station import StationNature


class TransferStationOut(Schema):
    name: str = Field(title="中转站名称", max_length=255)
    company: str = Field(tiele="公司名称", alias="company.name")
    street_code: str = Field(title="所属街道", alias="city_region.code")
    comm_code: str = Field(title="所属社区", alias="city_region.code")
    address: str = Field(title="地址", max_length=255)
    longitude: float = Field(None, title="经度")
    latitude: float = Field(None, title="维度")
    nature: StationNature = Field(title="场所性质", max_length=32)
    varieties: str = Field(title="经营品种", max_length=255)
    person_name: str = Field(title="负责人姓名", max_length=32)
    person_phone: str = Field(title="负责人联系方式", max_length=32)
