from django.core.paginator import Paginator
from django.db import transaction
from ninja import Query, Router
from ninja.errors import HttpError

from infra.decorators import permission_required
from infra.schemas import Pagination
from recycle.models import Company, Region, User, VehicleDraft
from recycle.models.region import RegionGrade
from recycle.models.vehicle_application import VehicleApplication
from recycle.models.vehicle_history import VehicleChangeType
from recycle.permissions import IsCompanyManager
from recycle.schemas.vehicle import VehicleIn
from recycle.schemas.vehicle_application import VehicleApplicationOut
from recycle.schemas.vehicle_draft import VehicleDraftOut

router = Router(tags=["车辆草稿"])


@router.post("", response={201: VehicleDraftOut})
@permission_required([IsCompanyManager])
def create_vehicle_draft(request, data: VehicleIn):
    """新增车辆草稿"""

    try:
        street = Region.objects.get(code=data.service_street_code, grade=RegionGrade.STREET)
    except Region.DoesNotExist:
        raise HttpError(404, "街道不存在")
    user: User = request.auth
    company = Company.objects.filter(manager__user=user).first()
    draft = VehicleDraft.objects.create(
        company=company,
        plate_number=data.plate_number,
        service_street=street,
        type=data.type,
        energy_type=data.energy_type,
        load=data.load,
        meet_spec=data.meet_spec,
    )
    return draft


@router.get("", response=Pagination[VehicleDraftOut])
@permission_required([IsCompanyManager])
def list_vehicle_draft(
    request,
    service_street_code: str = Query(None, title="服务街道编码"),
    plate_number: str = Query(None, title="车牌号"),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=20, gt=0, le=10000),
):
    """车辆草稿列表"""

    company = Company.objects.filter(manager__user=request.auth).first()
    queryset = VehicleDraft.objects.filter(company=company).select_related("service_street", "company").order_by("id")
    if service_street_code:
        queryset = queryset.filter(service_street__code=service_street_code)
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.put("/{id_}", response=VehicleDraftOut)
@permission_required([IsCompanyManager])
def update_vehicle_draft(request, id_: int, data: VehicleIn):
    company = Company.objects.filter(manager__user=request.auth).first()
    try:
        street = Region.objects.get(code=data.service_street_code, grade=RegionGrade.STREET)
        draft = VehicleDraft.objects.get(pk=id_, company=company)
    except Region.DoesNotExist:
        raise HttpError(404, "街道不存在")
    except VehicleDraft.DoesNotExist:
        raise HttpError(404, "草稿不存在")
    draft.plate_number = data.plate_number
    draft.service_street = street
    draft.type = data.type
    draft.energy_type = data.energy_type
    draft.load = data.load
    draft.meet_spec = data.meet_spec
    draft.save()
    return draft


@router.delete("/{id_}", response={204: None})
@permission_required([IsCompanyManager])
def delete_vehicle_draft(request, id_: int):
    """删除车辆草稿"""

    company = Company.objects.filter(manager__user=request.auth).first()
    try:
        VehicleDraft.objects.get(pk=id_, company=company).delete()
    except VehicleDraft.DoesNotExist:
        raise HttpError(404, "草稿不存在")


@router.post("/{id_}/application", response={201: VehicleApplicationOut})
@permission_required([IsCompanyManager])
def submit_vehicle_application(request, id_: int):
    """车辆草稿提交审批"""

    company = Company.objects.filter(manager__user=request.auth).first()
    try:
        draft = VehicleDraft.objects.get(pk=id_, company=company)
    except VehicleDraft.DoesNotExist:
        raise HttpError(404, "草稿不存在")

    with transaction.atomic():
        application = VehicleApplication.objects.create(
            company=draft.company,
            plate_number=draft.plate_number,
            service_street=draft.service_street,
            type=draft.type,
            energy_type=draft.energy_type,
            load=draft.load,
            meet_spec=draft.meet_spec,
            change_type=VehicleChangeType.NEW,
        )
        draft.delete()
    return application
