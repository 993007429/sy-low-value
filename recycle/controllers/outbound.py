from datetime import date, timedelta

from django.core.paginator import Paginator
from ninja import Query, Router
from ninja.errors import HttpError

from infra.schemas import Page, Pagination
from recycle.models import TransferStation
from recycle.models.outbound import OutboundRecord
from recycle.schemas.outbound import OutboundRecordIn, OutboundRecordOut

router = Router(tags=["出场记录"])


@router.get("", response=Pagination[OutboundRecordOut])
def list_outbound_records(
    request,
    start_date: date = Query(None, title="开始日期"),
    end_date: date = Query(None, title="截止日期"),
    plate_number: str = Query(None, title="车牌号"),
    category: str = Query(None, title="细分品类"),
    place_to_go: str = Query(None, title="去向"),
    page: Page = Query(...),
):
    """中转站出场记录"""

    queryset = OutboundRecord.objects.order_by("-id")
    if start_date:
        queryset = queryset.filter(net_weight_time__gte=start_date)
    if end_date:
        end_date = end_date + timedelta(days=1)
        queryset = queryset.filter(net_weight_time__lte=end_date)
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    if category:
        queryset = queryset.filter(category__contains=category)
    if place_to_go:
        queryset = queryset.filter(source_street_name__contains=place_to_go)

    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.post("", response={201: OutboundRecordOut})
def create_transfer_station_record(request, data: OutboundRecordIn):
    """添加出场记录"""

    try:
        station = TransferStation.objects.get(name=data.station_name)
    except TransferStation.DoesNotExist:
        raise HttpError(404, f"中转站 {data.station_name} 不存在")
    outbound = OutboundRecord.objects.create(
        station=station,
        plate_number=data.plate_number,
        driver=data.driver,
        weigher=data.weigher,
        carrier_name=data.carrier_name,
        tare_weight=data.tare_weight,
        gross_weight=data.gross_weight,
        net_weight=data.net_weight,
        tare_weight_time=data.tare_weight_time,
        gross_weight_time=data.gross_weight_time,
        net_weight_time=data.net_weight_time,
        recyclables_type=data.recyclables_type,
        category=data.category,
        plate_number_photo_in=data.plate_number_photo_in,
        vehicle_head_photo_in=data.vehicle_head_photo_in,
        vehicle_roof_photo_in=data.vehicle_roof_photo_in,
        plate_number_photo_out=data.plate_number_photo_out,
        vehicle_head_photo_out=data.vehicle_head_photo_out,
        vehicle_roof_photo_out=data.vehicle_roof_photo_out,
        place_to_go=data.place_to_go,
    )
    return outbound