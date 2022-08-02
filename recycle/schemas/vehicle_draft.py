from pydantic import Field

from recycle.schemas.vehicle import VehicleIn


class VehicleDraftOut(VehicleIn):
    id: int
    service_street_name: str = Field(None, title="服务街道名")
    company_name: str = Field(None, title="所属单位名")
    company_id: str
    vehicle_licence: str = Field(None, title="行驶证")
