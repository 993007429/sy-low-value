from datetime import date, timedelta
from typing import List

from django.db import IntegrityError
from django.db.models import F, Sum
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate

from infra.decorators import permission_required
from recycle.models import HazardousWasteCompany
from recycle.models.hazardous_waste_report import HazardousWasteReport
from recycle.permissions import IsHazardousWasterManager, IsPlatformManager
from recycle.schemas.hazardous_waste_report import (
    HazardousWasteReportIn,
    HazardousWasteReportOut,
    ThroughputByCompanyOut,
)

router = Router(tags=["有害垃圾填报"])


@router.get("", response=List[HazardousWasteReportOut])
@paginate(PageNumberPagination, page_size=20)
@permission_required([IsPlatformManager, IsHazardousWasterManager])
def list_hazardous_waste_reports(request, company_id: int = None, start_date: date = None, end_date: date = None):
    """查看有害垃圾填报记录"""

    queryset = HazardousWasteReport.objects.select_related("company").order_by("-report_date")
    company = HazardousWasteCompany.objects.filter(user=request.auth).first()
    if company:
        queryset = queryset.filter(company=company)  # 有害垃圾清运公司只能查看自己提交的记录
    if company_id:
        queryset = queryset.filter(company_id=company_id)
    if start_date:
        queryset = queryset.filter(report_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(report_date__lte=end_date)
    return queryset


@router.post("", response={201: HazardousWasteReportOut})
@permission_required([IsHazardousWasterManager])
def submit_hazardous_waste_report(request, data: HazardousWasteReportIn):
    """填报有害垃圾数据"""

    # 只能填报前两天的数据
    today = date.today()
    two_days_ago = today - timedelta(days=2)
    if not (two_days_ago <= data.report_date < today):
        raise HttpError(400, "只能填报昨天和前天的数据")
    company = HazardousWasteCompany.objects.get(user=request.auth)
    try:
        obj = HazardousWasteReport.objects.create(company=company, **data.dict())
    except IntegrityError:
        raise HttpError(409, f"{data.report_date} 已填报记录")
    return obj


@router.get("/throughput_by_company", response=List[ThroughputByCompanyOut])
@permission_required([IsPlatformManager])
def throughput_by_company(request, start_date: date = None, end_date: date = None):
    queryset = HazardousWasteReport.objects.all().select_related("company")
    if start_date:
        queryset = queryset.filter(report_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(report_date__lte=end_date)
    aggregations = (
        queryset.annotate(company_name=F("company__name"))
        .values("company_id", "company_name")
        .annotate(throughput=Sum("weight"))
    )
    for agg in aggregations:
        if not agg["throughput"]:
            agg["throughput"] = 0
    return aggregations
