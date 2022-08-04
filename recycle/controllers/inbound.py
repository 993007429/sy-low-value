from datetime import date, timedelta

from django.core.paginator import Paginator
from django.db.models import Sum
from ninja import Query, Router
from ninja.errors import HttpError

from infra.authentication import AgentAuth, AuthToken, LjflToken
from infra.schemas import Page
from recycle.models import Company, Event, TransferStation, User, Vehicle
from recycle.models.event import EventType
from recycle.models.inbound import InboundRecord
from recycle.schemas.inbound import InboundRecordIn, InboundRecordPaginationOut

router = Router(tags=["进场记录"])


@router.get("", response=InboundRecordPaginationOut, auth=[AuthToken(), LjflToken()])
def list_inbound_records(
    request,
    start_date: date = Query(None, description="开始日期"),
    end_date: date = Query(None, description="截止日期"),
    station_id: str = Query(None, description="可回收物中转站"),
    plate_number: str = Query(None, description="车牌号"),
    carrier_credit_code: str = Query(None, description="承运公司统一信用代码"),
    source_street: str = Query(None, description="来源街道"),
    page: Page = Query(...),
):
    """中转站进场记录"""

    queryset = InboundRecord.standing_book.prefetch_related("station", "carrier", "source_street").order_by("-id")
    # 公司用户只能查看本公司记录
    if isinstance(request.auth, User) and (company := Company.objects.filter(manager__user=request.auth).first()):
        queryset = queryset.filter(carrier=company)
    if start_date:
        queryset = queryset.filter(net_weight_time__gte=start_date)
    if end_date:
        end_date = end_date + timedelta(days=1)
        queryset = queryset.filter(net_weight_time__lt=end_date)
    if station_id:
        queryset = queryset.filter(station_id=station_id)
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    if carrier_credit_code:
        queryset = queryset.filter(carrier__uniform_social_credit_code=carrier_credit_code)
    if source_street:
        queryset = queryset.filter(source_street__code=source_street)

    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    aggregations = queryset.aggregate(total_weight=Sum("net_weight"))
    if (total_weight := aggregations["total_weight"]) is None:
        total_weight = 0
    return InboundRecordPaginationOut(count=paginator.count, total_weight=total_weight, results=list(p.object_list))


@router.post("", response={201: None}, auth=[AgentAuth()])
def create_transfer_station_record(request, data: InboundRecordIn):
    """添加进场记录"""

    try:
        station = TransferStation.objects.get(uuid=data.station_uuid)
        vehicle = Vehicle.objects.select_related("company").filter(plate_number=data.plate_number).first()
    except TransferStation.DoesNotExist:
        raise HttpError(404, f"中转站 {data.station_uuid} 不存在")
    defaults = dict(
        station=station,
        uuid=data.uuid,
        plate_number=data.plate_number,
        driver=data.driver,
        weigher=data.weigher,
        carrier=vehicle.company if vehicle else None,
        source_street=vehicle.service_street if vehicle else None,
        tare_weight=data.tare_weight,
        gross_weight=data.gross_weight,
        net_weight=data.net_weight,
        tare_weight_time=data.tare_weight_time,
        gross_weight_time=data.gross_weight_time,
        net_weight_time=data.net_weight_time,
        recyclables_type=data.recyclables_type,
        plate_number_photo_in=data.plate_number_photo_in,
        vehicle_head_photo_in=data.vehicle_head_photo_in,
        vehicle_roof_photo_in=data.vehicle_roof_photo_in,
        plate_number_photo_out=data.plate_number_photo_out,
        vehicle_head_photo_out=data.vehicle_head_photo_out,
        vehicle_roof_photo_out=data.vehicle_roof_photo_out,
    )
    inbound, created = InboundRecord.objects.update_or_create(defaults=defaults, uuid=data.uuid)
    # 检查是否超重 FIXME: 可以将数据发送到kafka, 将进站数据存储和异常检测解耦
    if vehicle and data.net_weight > vehicle.load * 1000 and created:
        Event.objects.create(
            plate_number=data.plate_number,
            started_at=data.net_weight_time,
            ended_at=data.net_weight_time,
            type=EventType.OVERLOAD,
        )
    return inbound
