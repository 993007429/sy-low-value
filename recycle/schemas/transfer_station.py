from ninja import ModelSchema, Schema
from pydantic import Field

from recycle.models.transfer_station import TransferStation


class TransferStationOut(ModelSchema):
    street_code: str = Field(None, title="所属街道编码", alias="street.code")
    street_name: str = Field(None, title="所属街道名称", alias="street.name")
    community_code: str = Field(title="所属社区", alias="community.code")
    community_name: str = Field(title="所属社区", alias="community.name")

    class Config:
        model = TransferStation
        model_fields = [
            "name",
            "management_company",
            "address",
            "longitude",
            "latitude",
            "nature",
            "varieties",
            "manager_name",
            "manager_phone",
        ]


class TransferStationImportOut(Schema):
    imported_count: int = Field(None, title="导入中转站数量")
