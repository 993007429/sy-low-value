from datetime import date, timedelta
from typing import List

from dateutil.relativedelta import relativedelta
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth
from ninja import Query, Router

from recycle.models import InboundRecord
from recycle.schemas.inbound_statistics import (
    ThroughputByStationOut,
    ThroughputOut,
    ThroughputTrendDailyOut,
    ThroughputTrendMonthlyOut,
)

router = Router(tags=["进场统计"])


@router.get("/throughput", response=ThroughputOut)
def calc_throughput(request, start_date: date, end_date: date, street_code: str = None):
    """进场可回收物处理量"""

    end_date = end_date + timedelta(days=1)
    queryset = InboundRecord.objects.filter(net_weight_time__gte=start_date, net_weight_time__lt=end_date)
    if street_code:
        queryset = queryset.filter(station__street__code=street_code)
    aggregations = queryset.aggregate(throughput=Sum("net_weight"))
    if not aggregations["throughput"]:  # sum没有值时会返回None
        aggregations["throughput"] = 0
    return aggregations


@router.get("/throughput-by-station", response=List[ThroughputByStationOut])
def calc_throughput_by_station(request, start_date: date, end_date: date, street_code: str = None):
    """按照中转站统计进场量"""

    end_date = end_date + timedelta(days=1)
    queryset = InboundRecord.objects.filter(net_weight_time__gte=start_date, net_weight_time__lt=end_date)
    if street_code:
        queryset = queryset.filter(station__street__code=street_code)
    aggregations = (
        queryset.annotate(station_name=F("station__name"))
        .values("station_id", "station_name")
        .annotate(throughput=Sum("net_weight"), count=Count("*"))
        .order_by("-throughput")
    )
    for agg in aggregations:
        if not agg["throughput"]:  # sum没有值时会返回None
            agg["throughput"] = 0

    return aggregations


@router.get("/throughput-trend-daily", response=List[ThroughputTrendDailyOut])
def calc_throughput_trend_daily(
    request, day: date, street_code: str = None, station_id: str = Query(None, description="中转站")
):
    """统计最近七日进场量趋势"""

    end_date = day + timedelta(days=1)
    start_date = end_date - timedelta(days=7)
    queryset = InboundRecord.objects.filter(net_weight_time__gte=start_date, net_weight_time__lt=end_date)
    if street_code:
        queryset = queryset.filter(station__street__code=street_code)
    if station_id:
        queryset = queryset.filter(station_id=station_id)
    aggregations = (
        queryset.annotate(day=F("net_weight_time__date"))
        .values("day")
        .annotate(throughput=Sum("net_weight"))
        .order_by("day")
    )
    for agg in aggregations:
        if not agg["throughput"]:  # sum没有值时会返回None
            agg["throughput"] = 0

    return aggregations


@router.get("/throughput-trend-monthly", response=List[ThroughputTrendMonthlyOut])
def calc_throughput_trend_monthly(
    request, year: int, month: int, street_code: str = None, station_id: str = Query(None, description="中转站")
):
    """统计最近七月进场量趋势"""

    end_date = date(year, month, 1) + relativedelta(months=1)
    start_date = end_date - relativedelta(months=7)
    queryset = InboundRecord.objects.filter(net_weight_time__gte=start_date, net_weight_time__lt=end_date)
    if street_code:
        queryset = queryset.filter(station__street__code=street_code)
    if station_id:
        queryset = queryset.filter(station_id=station_id)
    aggregations = (
        queryset.annotate(month=TruncMonth("net_weight_time"))
        .values("month")
        .annotate(throughput=Sum("net_weight"))
        .order_by("month")
    )
    for agg in aggregations:
        if not agg["throughput"]:  # sum没有值时会返回None
            agg["throughput"] = 0

    return aggregations
