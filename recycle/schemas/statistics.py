from ninja import Schema
from pydantic import Field


class GeneralInformationOut(Schema):
    companies_count: int = Field(title="清运公司总数")
    vehicles_count: int = Field(title="车辆总数")
    stations_count: int = Field(title="中转站总数")


class ScopePointOut(Schema):
    scope_code: str = Field(title="地区编码")
    scope_name: str = Field(title="地区名称")
    lon_lat: str = Field(title="地区名称")
    lon_center: float = Field(title="中心点经度")
    lat_center: float = Field(title="中心点维度")
    is_null: int = Field(title="")


class ThroughputByStreetOut(Schema):
    source_street_name: str = Field(title="来源街道")
    net_weight__sum: float = Field(title="可回收物处理重量")


class ThroughputByStreetAndStationOut(Schema):
    source_street_name: str = Field(title="来源街道")
    station: str = Field(title="中转站名称")
    recyclables_type: str = Field(title="可回收物类型")
    net_weight__sum: float = Field(title="可回收物处理重量")
