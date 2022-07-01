from django.core.paginator import Paginator
from django.db import IntegrityError
from ninja import Query, Router
from ninja.errors import HttpError

from infra.schemas import Pagination
from recycle.models import Company, Region, RegionGrade, User, Vehicle
from recycle.schemas.vehicle import VehicleIn, VehicleOut

router = Router(tags=["车辆台帐"])


@router.post("", response={201: VehicleOut})
def create_vehicle(request, data: VehicleIn):
    """新增车辆"""

    try:
        street = Region.objects.get(code=data.service_street_code, grade=RegionGrade.STREET)
    except Region.DoesNotExist:
        raise HttpError(404, "街道不存在")
    user: User = request.auth
    company = Company.objects.get(uniform_social_credit_code=user.username)
    try:
        vehicle = Vehicle.objects.create(
            company=company,
            plate_number=data.plate_number,
            service_street=street,
            type=data.type,
            energy_type=data.energy_type,
            load=data.load,
            meet_spec=data.meet_spec,
        )
    except IntegrityError:
        raise HttpError(409, "车辆已存在")
    return vehicle


@router.get("", response=Pagination[VehicleOut], auth=None)
def list_vehicle(
    request,
    service_street_code: str = Query(None, title="服务街道编码"),
    plate_number: str = Query(None, title="车牌号"),
    company_id: str = Query(None, title="所属公司"),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=20, gt=0, le=10000),
):
    """车辆列表"""
    # TODO: 权限限制。 # FIXME: 暂时放开认证只能这么些，直接REQUEST.AUTH会报错
    user: User = getattr(request, "auth", None)
    company = Company.objects.filter(manager__user=user).first()
    if company:  # 如果是公司用户则只能查看自己公司名下的车
        company_id = company.id
    queryset = Vehicle.objects.all().select_related("service_street", "company").order_by("id")
    if service_street_code:
        queryset = queryset.filter(service_street__code=service_street_code)
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    if company_id:
        queryset = queryset.filter(company_id=company_id)
    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.put("/{id_}", response=VehicleOut)
def update_vehicle(request, id_: int, data: VehicleIn):
    try:
        street = Region.objects.get(code=data.service_street_code, grade=RegionGrade.STREET)
        vehicle = Vehicle.objects.get(pk=id_)
    except Region.DoesNotExist:
        raise HttpError(404, "街道不存在")
    except Vehicle.DoesNotExist:
        raise HttpError(404, "车辆不存在")
    vehicle.plate_number = data.plate_number
    vehicle.service_street = street
    vehicle.type = data.type
    vehicle.energy_type = data.energy_type
    vehicle.load = data.load
    vehicle.meet_spec = data.meet_spec
    try:
        vehicle.save()
    except IntegrityError:
        raise HttpError(409, "车辆已存在")
    return vehicle


@router.delete("/{id_}", response={204: None})
def delete_vehicle(request, id_: int):
    try:
        Vehicle.objects.get(pk=id_).delete()
    except Vehicle.DoesNotExist:
        raise HttpError(404, "车辆不存在")
