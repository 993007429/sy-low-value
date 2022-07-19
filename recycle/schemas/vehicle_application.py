from datetime import datetime
from typing import Literal

from ninja import Schema
from pydantic import BaseModel, Field, validator

from recycle.models.vehicle import EnergyType, VehicleType
from recycle.models.vehicle_application import ApprovalState
from recycle.models.vehicle_history import VehicleChangeType


class VehicleApplicationOperationIn(BaseModel):
    state: Literal[ApprovalState.APPROVED, ApprovalState.REJECTED] = Field(..., title="审核状态")
    reason: str = Field(None, title="审核拒绝原因")

    @validator("reason")
    def validate_reason(cls, reason, values):
        if values["state"] == ApprovalState.REJECTED and not reason:
            raise ValueError("reason must not be empty when state is REJECTED")
        return reason


class VehicleApplicationOut(Schema):
    id: int
    plate_number: str = Field(..., title="车牌号", max_length=32)
    service_street_code: str = Field(..., title="服务街道编码", max_length=32)
    type: VehicleType = Field(..., title="车辆类型")
    energy_type: EnergyType = Field(..., title="能源类型")
    load: float = Field(..., title="载重量", gt=0)
    meet_spec: bool = Field(..., title="是否按规范喷涂")
    service_street_name: str = Field(None, title="服务街道名")
    company_name: str = Field(None, title="所属单位名")
    company_id: str

    change_type: VehicleChangeType = Field(..., title="变更类型")
    state: ApprovalState = Field(None, title="审核状态")
    reason: str = Field(None, title="审核拒绝原因")
    applied_at: datetime = Field(None, title="申请时间", alias="created_at")
    processed_at: datetime = Field(None, title="审核时间")
