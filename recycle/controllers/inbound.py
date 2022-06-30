from datetime import date, timedelta

from django.core.paginator import Paginator
from ninja import Query, Router
from ninja.errors import HttpError

from infra.schemas import Page, Pagination
from recycle.models import TransferStation, Vehicle
from recycle.models.inbound import InboundRecord
from recycle.schemas.inbound import InboundRecordIn, InboundRecordOut

router = Router(tags=["进场记录"])


@router.get("", response=Pagination[InboundRecordOut])
def list_inbound_records(
    request,
    start_date: date = Query(None, title="开始日期"),
    end_date: date = Query(None, title="截止日期"),
    plate_number: str = Query(None, title="车牌号"),
    carrier_credit_code: str = Query(None, title="承运公司统一信用代码"),
    source_street: str = Query(None, title="来源街道"),
    page: Page = Query(...),
):
    """中转站进场记录"""

    queryset = InboundRecord.objects.order_by("-id")
    if start_date:
        queryset = queryset.filter(net_weight_time__gte=start_date)
    if end_date:
        end_date = end_date + timedelta(days=1)
        queryset = queryset.filter(net_weight_time__lte=end_date)
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    if carrier_credit_code:
        queryset = queryset.filter(carrier__uniform_social_credit_code=carrier_credit_code)
    if source_street:
        queryset = queryset.filter(source_street_name__contains=source_street)

    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.post("", response={201: InboundRecordOut})
def create_transfer_station_record(request, data: InboundRecordIn):
    """添加进场记录"""

    try:
        station = TransferStation.objects.get(name=data.station_name)
        vehicle = Vehicle.objects.select_related("company").get(plate_number=data.plate_number)
    except TransferStation.DoesNotExist:
        raise HttpError(404, f"中转站 {data.station_name} 不存在")
    except Vehicle.DoesNotExist:
        raise HttpError(404, f"运输车辆 {data.plate_number} 不存在")
    inbound = InboundRecord.objects.create(
        station=station,
        plate_number=data.plate_number,
        driver=data.driver,
        weigher=data.weigher,
        carrier=vehicle.company,
        carrier_name=data.carrier_name,
        source_street_name=data.source_street_name,
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
    return inbound
