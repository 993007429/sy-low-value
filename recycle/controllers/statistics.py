from datetime import date, timedelta
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F, Sum
from ninja import Query, Router
from ninja.errors import HttpError

from recycle.models import Company, HighValueReport, InboundRecord, Region, TransferStation, Vehicle
from recycle.schemas.statistics import CountByStreetOut, GeneralInformationOut, HighLowValueThroughputByDay

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


@router.get("/high-low-value-throughput-by-day", response=List[HighLowValueThroughputByDay])
def get_high_low_value_throughput_by_day(request, start_date: date, end_date: date):
    """按天统计高低值总量"""

    low_values = InboundRecord.standing_book.all()
    high_values = HighValueReport.objects.all().select_related("street")

    if start_date:
        low_values = low_values.filter(net_weight_time__date__gte=start_date)
        high_values = high_values.filter(report_date__gte=start_date)
    if end_date:
        low_values = low_values.filter(net_weight_time__date__lte=end_date)
        high_values = high_values.filter(report_date__lte=end_date)
    low_value_aggregations = (
        low_values.annotate(date=F("net_weight_time__date")).values("date").annotate(throughput=Sum("net_weight"))
    )
    high_value_aggregations = (
        high_values.annotate(date=F("report_date")).values("date").annotate(throughput=Sum("high_value_weight"))
    )

    results = []
    day = start_date
    while day <= end_date:
        high_value = 0
        low_value = 0
        for agg in high_value_aggregations:
            if agg["date"] == day:
                high_value = agg["throughput"] or 0
                break
        for agg in low_value_aggregations:
            if agg["date"] == day:
                high_value = agg["throughput"] or 0
                break
        results.append(HighLowValueThroughputByDay(day=day, high_value=high_value, low_value=low_value))
        day = day + timedelta(days=1)
    return results
