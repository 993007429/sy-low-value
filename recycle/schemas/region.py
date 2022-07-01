from ninja import Schema
from pydantic import Field


class RegionOut(Schema):
    code: str
    name: str


class RegionScopeOut(Schema):
    region_code: str = Field(title="地区编码")
    region_name: str = Field(title="地区名称")
    lon_lat: str = Field(title="地区名称")
    lon_center: float = Field(title="中心点经度")
    lat_center: float = Field(title="中心点维度")
    is_null: int = Field(title="")
