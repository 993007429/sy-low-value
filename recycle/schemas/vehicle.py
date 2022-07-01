from ninja import Schema
from pydantic import Field

from recycle.models import EnergyType, VehicleType


class VehicleIn(Schema):
    plate_number: str = Field(..., title="车牌号", max_length=32)
    service_street_code: str = Field(..., title="服务街道编码", max_length=32)
    type: VehicleType = Field(..., title="车辆类型")
    energy_type: EnergyType = Field(..., title="能源类型")
    load: float = Field(..., title="载重量", gt=0)
    meet_spec: bool = Field(..., title="是否按规范喷涂")


class VehicleOut(VehicleIn):
    id: int
    service_street_name: str = Field(None, title="服务街道名")
    company_name: str = Field(None, title="所属单位名")
    company_id: str
