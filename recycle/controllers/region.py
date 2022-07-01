from typing import List

from django.conf import settings
from ninja import Router

from infra.utils import center_geo, get_zone_range
from recycle.models import Region, RegionGrade
from recycle.models.region_scope import RegionScope
from recycle.schemas.region import RegionOut, RegionScopeOut

router = Router(tags=["区域"])


@router.get("/area", auth=None, response=List[RegionOut])
def list_areas(request):
    """区列表"""

    regions = Region.objects.filter(grade=RegionGrade.AREA)
    return regions


@router.get("/street", response=List[RegionOut])
def list_streets(request):
    """街道列表"""

    regions = Region.objects.filter(parent__code=settings.REGION_CODE, grade=RegionGrade.STREET).order_by("code")
    return regions


@router.get("/region-scope", response=List[RegionScopeOut])
def scope_point(request, area_code: str = settings.REGION_CODE):
    """区域点位信息"""

    _scope = "street"
    grade, zone_start, zone_end = get_zone_range(area_code)
    scope_qs = RegionScope.objects.filter(code__gte=zone_start, code__lt=zone_end)

    attr_dict = {
        "street": ["code", "name"],
    }

    return_list = list()
    _scope_attr = attr_dict.get(_scope)
    for scope in scope_qs:
        region_code = getattr(scope, _scope_attr[0])
        region_name = getattr(scope, _scope_attr[1])

        lon_center = scope.lon_center
        lat_center = scope.lat_center
        lon_lat = scope.lon_lat
        is_null = scope.is_null

        if not lon_center and not lat_center:
            tem_list = []
            lon_la_list = lon_lat.split(";")
            for i in lon_la_list:
                tem_list.append([float(i.split(",")[0]), float(i.split(",")[1])])

            lon_center, lat_center = center_geo(tem_list)
        return_list.append(
            RegionScopeOut(
                region_code=region_code,
                region_name=region_name,
                lon_lat=lon_lat,
                lon_center=lon_center,
                lat_center=lat_center,
                is_null=is_null,
            )
        )
    return return_list
