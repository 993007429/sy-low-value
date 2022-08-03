from ninja import Schema
from pydantic import Field


class GeneralInformationOut(Schema):
    companies_count: int = Field(title="清运公司总数")
    vehicles_count: int = Field(title="车辆总数")
    stations_count: int = Field(title="中转站总数")


class CountByStreetOut(Schema):
    service_street_code: str = Field(title="街道编码")
    service_street_name: str = Field(title="街道名")
    vehicles_count: int = Field(title="服务车辆数")
    companies_count: int = Field(title="服务公司数")
