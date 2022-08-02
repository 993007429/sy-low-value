from ninja import Schema
from pydantic import AnyHttpUrl, Field

from recycle.models.vehicle import EnergyType, VehicleType


class VehicleIn(Schema):
    plate_number: str = Field(..., title="车牌号", max_length=32)
    service_street_code: str = Field(..., title="服务街道编码", max_length=32)
    type: VehicleType = Field(..., title="车辆类型")
    energy_type: EnergyType = Field(..., title="能源类型")
    load: float = Field(..., title="载重量", gt=0)
    meet_spec: bool = Field(..., title="是否按规范喷涂")
    vehicle_licence: AnyHttpUrl = Field(..., title="行驶证")


class VehicleOut(VehicleIn):
    id: int
    vehicle_licence: str = Field(None, title="行驶证")
    service_street_name: str = Field(None, title="服务街道名")
    company_name: str = Field(None, title="所属单位名")
    company_id: str
    longitude: float = Field(None, title="经度")
    latitude: float = Field(None, title="纬度")
    longitude_gcj02: float = Field(None, title="gcj02坐标系经度，适用高德地图")
    latitude_gcj02: float = Field(None, title="gcj02坐标系纬度，适用高德地图")
