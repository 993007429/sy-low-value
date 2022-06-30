from datetime import date, timedelta

from django.db.models import Sum
from ninja import Router

from recycle.models import InboundRecord
from recycle.schemas.inbound_statistics import ThroughputOut

router = Router(tags=["进场统计"])


@router.get("/throughput", response=ThroughputOut)
def throughput(request, start_date: date, end_date: date, street_code: str = None):
    """进场可回收物处理量"""

    end_date = end_date + timedelta(days=1)
    queryset = InboundRecord.objects.filter(net_weight_time__gte=start_date, net_weight_time__lt=end_date)
    if street_code:
        queryset = queryset.filter(station__street__code=street_code)
    aggregations = queryset.aggregate(throughput=Sum("net_weight"))
    if not aggregations["throughput"]:  # sum没有值时会返回None
        aggregations["throughput"] = 0
    return aggregations
