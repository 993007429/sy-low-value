from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Sum
from ninja import Query, Router
from ninja.errors import HttpError

from infra.schemas import Page, Pagination
from infra.utils import center_geo, get_zone_range
from recycle.models import Company, InboundRecord, Region, TransferStation, Vehicle
from recycle.models.region_scope import RegionScope
from recycle.schemas.statistics import (
    GeneralInformationOut,
    ScopePointOut,
    ThroughputByStreetAndStationOut,
    ThroughputByStreetOut,
)

router = Router(tags=["基本信息、地区范围点位、各街道处理量"])


@router.get("/general-information", response={200: GeneralInformationOut})
def general_information(request, street_code: str = Query(None, description="街道编号")):
    """基本信息：清运公司总数、车辆总数、中转站总数"""

    companies = Company.objects.all()
    vehicles = Vehicle.objects.all()
    stations = TransferStation.objects.all()

    if street_code:
        try:
            street = Region.objects.get(code=street_code)
        except ObjectDoesNotExist:
            raise HttpError(404, f"街道不存在：{street_code}")
        vehicles = vehicles.filter(service_street=street)
        stations = stations.filter(street=street)

    return {
        "companies_count": companies.count(),
        "vehicles_count": vehicles.count(),
        "stations_count": stations.count(),
    }


@router.get("/scope-point", response=list[ScopePointOut])
def scope_point(request, area_code: str = "110113000000"):
    """顺义区街道点位信息"""

    _scope = "street"
    grade, zone_start, zone_end = get_zone_range(area_code)
    scope_qs = RegionScope.objects.filter(code__gte=zone_start, code__lt=zone_end)

    attr_dict = {
        "area": ["area_coding", "area_name"],
        "street": ["street_coding", "street_name"],
        "comm": ["comm_coding", "comm_name"],
    }

    return_list = list()
    _scope_attr = attr_dict.get(_scope)
    for scope in scope_qs:
        scope_code = getattr(scope, _scope_attr[0])
        scope_name = getattr(scope, _scope_attr[1])

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
            {
                "scope_code": str(scope_code),
                "scope_name": scope_name,
                "lon_lat": lon_lat,
                "lon_center": lon_center,
                "lat_center": lat_center,
                "is_null": is_null,
            }
        )
    return return_list


@router.get("throughput-by-street", response=list[ThroughputByStreetOut])
def cal_throughput_by_street(
    request,
    start_date: date = None,
    end_date: date = None,
):
    """各街道处理量"""

    records = InboundRecord.objects.all()
    if start_date and end_date:
        records = records.filter(net_weight_time__date__gte=start_date, net_weight_time__date__lte=end_date)
    result = records.values("source_street_name").annotate(Sum("net_weight"))
    return result


@router.get("throughput-by-street-and-station", response=Pagination[ThroughputByStreetAndStationOut])
def cal_throughput_by_street_and_station(
    request,
    start_date: date = None,
    end_date: date = None,
    page: Page = Query(...),
):
    """按中转站统计各街道处理量"""

    records = InboundRecord.objects.all()
    if start_date and end_date:
        records = records.filter(net_weight_time__date__gte=start_date, net_weight_time__date__lte=end_date)
    result = records.values("source_street_name", "station", "recyclables_type").annotate(Sum("net_weight"))
    paginator = Paginator(result, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}
