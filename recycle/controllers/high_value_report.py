from datetime import date, timedelta
from typing import List

from django.db import IntegrityError
from django.db.models import F, Sum
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate

from infra.decorators import permission_required
from recycle.models import PlatformManager
from recycle.models.high_value_report import HighValueReport
from recycle.permissions import IsPlatformManager, IsStreetManager
from recycle.schemas.high_value_report import HighValueReportIn, HighValueReportOut, ThroughputByStreetOut

router = Router(tags=["高值填报"])


@router.get("", response=List[HighValueReportOut])
@paginate(PageNumberPagination, page_size=20)
@permission_required([IsPlatformManager])
def list_high_value_reports(request, street_id: int = None, start_date: date = None, end_date: date = None):
    """查看高值填报记录"""

    queryset = HighValueReport.objects.select_related("street").order_by("-report_date")
    street_manager = PlatformManager.objects.filter(user=request.auth, role=PlatformManager.STREET).first()
    if street_manager:
        queryset = queryset.filter(street__code=street_manager.region_id)  # 街道只能查看自己提交的记录
    if street_id:
        queryset = queryset.filter(street_id=street_id)
    if start_date:
        queryset = queryset.filter(report_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(report_date__lte=end_date)
    return queryset


@router.post("", response={201: HighValueReportOut})
@permission_required([IsStreetManager])
def submit_high_value_report(request, data: HighValueReportIn):
    """填报高值数据"""

    # 只能填报前两天的数据
    today = date.today()
    two_days_ago = today - timedelta(days=2)
    if not (two_days_ago <= data.report_date < today):
        raise HttpError(400, "只能填报昨天和前天的数据")
    pm = PlatformManager.objects.select_related("region").get(user=request.auth)
    try:
        obj = HighValueReport.objects.create(street=pm.region, **data.dict())
    except IntegrityError:
        raise HttpError(409, f"{data.report_date} 已填报记录")
    return obj


@router.get("/throughput_by_street", response=List[ThroughputByStreetOut])
def throughput_by_street(request, start_date: date = None, end_date: date = None):
    queryset = HighValueReport.objects.all().select_related("street")
    if start_date:
        queryset = queryset.filter(report_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(report_date__lte=end_date)
    aggregations = (
        queryset.annotate(street_name=F("street__name"), street_code=F("street__code"))
        .values("street_code", "street_name")
        .annotate(throughput=Sum("high_value_weight"))
    )
    for agg in aggregations:
        if not agg["throughput"]:
            agg["throughput"] = 0
    return aggregations
