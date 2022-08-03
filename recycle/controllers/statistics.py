from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F
from ninja import Query, Router
from ninja.errors import HttpError

from recycle.models import Company, Region, TransferStation, Vehicle
from recycle.schemas.statistics import CountByStreetOut, GeneralInformationOut

router = Router(tags=["基本信息"])


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

    return GeneralInformationOut(
        companies_count=companies.count(), vehicles_count=vehicles.count(), stations_count=stations.count()
    )


@router.get("/count-by-street", response=List[CountByStreetOut])
def calc_count_by_street(request):
    """各街道服务车辆数量和服务单位数量"""

    count_by_street = (
        Vehicle.objects.annotate(
            service_street_code=F("service_street__code"), service_street_name=F("service_street__name")
        )
        .values("service_street_code", "service_street_name")
        .annotate(vehicles_count=Count("service_street_id"), companies_count=Count("company_id", distinct=True))
        .order_by("-vehicles_count")
    )

    return count_by_street
