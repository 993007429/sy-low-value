from datetime import datetime

from ninja import Schema
from pydantic import Field

from recycle.models.vehicle import EnergyType, VehicleType
from recycle.models.vehicle_history import VehicleChangeType


class VehicleHistoryOut(Schema):
    id: int
    plate_number: str = Field(..., title="车牌号", max_length=32)
    service_street_code: str = Field(..., title="服务街道编码", max_length=32)
    service_street_name: str = Field(None, title="服务街道名")
    type: VehicleType = Field(..., title="车辆类型")
    energy_type: EnergyType = Field(..., title="能源类型")
    load: float = Field(..., title="载重量", gt=0)
    meet_spec: bool = Field(..., title="是否按规范喷涂")
    company_name: str = Field(None, title="所属单位名")
    company_id: str
    vehicle_licence: str = Field(None, title="行驶证")
    change_type: VehicleChangeType = Field(None, title="变更类型")
    created_at: datetime = Field(None, title="变更时间")
