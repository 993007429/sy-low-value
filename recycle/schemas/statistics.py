from ninja import Schema
from pydantic import Field


class GeneralInformationOut(Schema):
    companies_count: int = Field(title="清运公司总数")
    vehicles_count: int = Field(title="车辆总数")
    stations_count: int = Field(title="中转站总数")
