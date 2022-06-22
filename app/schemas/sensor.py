from ninja import ModelSchema
from pydantic import Field

from app.models import Sensor


class SensorOut(ModelSchema):
    toilet_id: int
    terminal_id: str = Field(None, alias="toilet.terminal_id")
    toilet_name: str = Field(None, alias="toilet.name")
    toilet_management: str = Field(None, alias="toilet.management.name", description="管理单位")
    toilet_address: str = Field(None, alias="toilet.address")
    is_online: bool

    class Config:
        model = Sensor
        model_fields = [
            "id",
            "sensor_id",
            "sensor_type",
            "installation_location",
            "serial",
            "last_communication_time",
        ]
