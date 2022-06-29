from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from ninja import Query, Router
from ninja.errors import HttpError

from infra.schemas import Page, Pagination
from recycle.models import Company, RecordInbound, RecordOutbound, TransferStation, Vehicle
from recycle.schemas.record import RecordInboundIn, RecordInboundOut, RecordOutboundIn, RecordOutboundOut

router = Router(tags=["进出场记录"])


@router.get("/inbound", response=Pagination[RecordInboundOut])
def list_record_inbounds(
    request,
    company: str = Query(None, title="运营公司名称"),
    plate_number: str = Query(None, title="车牌号"),
    went: str = Query(None, title="去向"),
    start_date: date = Query(None, title="开始日期"),
    end_date: date = Query(None, title="截止日期"),
    page: Page = Query(...),
):
    """进场记录"""

    records = RecordInbound.objects.all()
    if company:
        records = records.filter(company__contains=company)
    if plate_number:
        records = records.filter(plate_number=plate_number)
    if went:
        records = records.filter(went__contains=went)
    if start_date and end_date:
        records = records.filter(inbound_time__date__gte=start_date, end_datetime_date__lte=end_date)
    paginator = Paginator(records, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.get("/outbound", response=Pagination[RecordOutboundOut])
def list_record_outbounds(
    request,
    start_date: date = Query(None, title="开始日期"),
    end_date: date = Query(None, title="截止日期"),
    source_street: str = Query(None, title="来源街道"),
    company: str = Query(None, title="运营公司"),
    page: Page = Query(...),
):
    """出场记录"""

    records = RecordOutbound.objects.all()
    if source_street:
        records = records.filter(source_street=source_street)
    if company:
        records = records.filter(company__contains=company)
    if start_date and end_date:
        records = records.filter(inbound_time__date__gte=start_date, end_datetime_date__lte=end_date)
    paginator = Paginator(records, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.post("/inbound", response={201: RecordInboundOut})
def create_record_inbounds(request, record_in: RecordInboundIn):
    """添加进场记录"""

    # 数据一致性检查：中转站台账、清运公司台账、清运车辆台账
    try:
        TransferStation.objects.get(name=record_in.station)
    except ObjectDoesNotExist:
        raise HttpError(409, f"进场记录数据错误：中转站 {record_in.station} 不存在")
    try:
        Company.objects.get(name=record_in.company)
    except ObjectDoesNotExist:
        raise HttpError(409, f"进场记录数据错误：清运公司 {record_in.company} 不存在")
    try:
        Vehicle.objects.get(plate_number=record_in.plate_number)
    except ObjectDoesNotExist:
        raise HttpError(409, f"进场记录数据错误：运输车辆 {record_in.plate_number} 不存在")
    record = RecordInbound.objects.create(**record_in.dict())
    return record


@router.post("/outbound", response={201: RecordOutboundOut})
def create_record_outbounds(request, record_in: RecordOutboundIn):
    """添加出场记录"""

    # 数据一致性检查：中转站台账、清运公司台账、清运车辆台账
    try:
        TransferStation.objects.get(name=record_in.station)
    except ObjectDoesNotExist:
        raise HttpError(409, f"进场记录数据错误：中转站 {record_in.station} 不存在")
    try:
        Company.objects.get(name=record_in.company)
    except ObjectDoesNotExist:
        raise HttpError(409, f"进场记录数据错误：清运公司 {record_in.company} 不存在")
    try:
        Vehicle.objects.get(plate_number=record_in.plate_number)
    except ObjectDoesNotExist:
        raise HttpError(409, f"进场记录数据错误：运输车辆 {record_in.plate_number} 不存在")
    record = RecordOutbound.objects.create(**record_in.dict())
    return record
