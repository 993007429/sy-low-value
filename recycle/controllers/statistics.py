from django.core.exceptions import ObjectDoesNotExist
from ninja import Query, Router
from ninja.errors import HttpError

from recycle.models import Company, Region, TransferStation, Vehicle
from recycle.schemas.statistics import GeneralInformationOut

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

    return {
        "companies_count": companies.count(),
        "vehicles_count": vehicles.count(),
        "stations_count": stations.count(),
    }
