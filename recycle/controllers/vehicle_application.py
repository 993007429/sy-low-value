from datetime import date

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.utils import timezone
from ninja import Query, Router
from ninja.errors import HttpError

from infra.decorators import permission_required
from infra.schemas import Pagination
from recycle.models import Company, PlatformManager, Region, Vehicle, VehicleHistory
from recycle.models.region import RegionGrade
from recycle.models.vehicle_application import ApprovalState, VehicleApplication
from recycle.models.vehicle_history import VehicleChangeType
from recycle.permissions import IsCompanyManager, IsStreetManager
from recycle.schemas.vehicle import VehicleIn
from recycle.schemas.vehicle_application import VehicleApplicationOperationIn, VehicleApplicationOut

router = Router(tags=["车辆审核"])


@router.get("", response=Pagination[VehicleApplicationOut])
def list_vehicle_application(
    request,
    service_street_code: str = Query(None, title="服务街道编码"),
    plate_number: str = Query(None, title="车牌号"),
    state: ApprovalState = Query(None, title="审核状态"),
    start_date: date = Query(None, title="提交开始时间"),
    end_date: date = Query(None, title="提交结束时间"),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=20, gt=0, le=10000),
):
    """车辆审核列表"""

    queryset = VehicleApplication.objects.select_related("service_street", "company").order_by("-id")
    if c := Company.objects.filter(manager__user=request.auth).first():
        # 公司用只能查看自己提的审批
        queryset = queryset.filter(company=c)
    elif pm := PlatformManager.objects.filter(user=request.auth, role=PlatformManager.STREET).first():
        # 街道只能看到自己负责的审批
        queryset = queryset.filter(service_street=pm.region)
    if service_street_code:
        queryset = queryset.filter(service_street__code=service_street_code)
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    if state:
        queryset = queryset.filter(state=state)
    if start_date:
        queryset = queryset.filter(created_at__date__gte=start_date)
    if end_date:
        queryset = queryset.filter(created_at__date__lte=end_date)
    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.post("/{id_}/submit", response={201: VehicleApplicationOut})
@permission_required([IsCompanyManager])
def submit_vehicle_application(request, id_: int, data: VehicleIn):
    """车辆审批重新编辑提交，只有审批拒绝后才能重新提交"""

    company = Company.objects.get(manager__user=request.auth)
    try:
        rejected = VehicleApplication.objects.get(company=company, pk=id_, state=ApprovalState.REJECTED)
        street = Region.objects.get(code=data.service_street_code, grade=RegionGrade.STREET)
        with transaction.atomic():
            application = VehicleApplication.objects.create(
                company=rejected.company,
                plate_number=rejected.plate_number,
                service_street=street,
                type=data.type,
                energy_type=data.energy_type,
                load=data.load,
                meet_spec=data.meet_spec,
                change_type=rejected.change_type,
            )
            rejected.delete()  # 如果以后改为保留被拒绝的记录，删掉此行即可
    except VehicleApplication.DoesNotExist:
        raise HttpError(404, "审批不存在")
    except Region.DoesNotExist:
        raise HttpError(404, "街道不存在")
    return application


@router.patch("/{id_}", response={201: VehicleApplicationOut})
@permission_required([IsStreetManager])
def process_vehicle_application(request, id_: int, data: VehicleApplicationOperationIn):
    """审批车辆变更"""

    pm = PlatformManager.objects.select_related("region").get(user=request.auth)
    try:
        with transaction.atomic():
            application: VehicleApplication = VehicleApplication.objects.select_for_update().get(
                pk=id_, state=ApprovalState.APPROVING, service_street=pm.region
            )
            application.state = data.state
            application.processed_at = timezone.now()
            if data.state == ApprovalState.REJECTED:
                application.reason = data.reason
            if application.state == ApprovalState.APPROVED:
                # 保存、更新车辆台帐
                if application.change_type == VehicleChangeType.NEW:
                    Vehicle.objects.create(
                        company=application.company,
                        plate_number=application.plate_number,
                        service_street=application.service_street,
                        type=application.type,
                        energy_type=application.energy_type,
                        load=application.load,
                        meet_spec=application.meet_spec,
                    )
                elif application.change_type == VehicleChangeType.CHANGE:
                    vehicle = Vehicle.objects.get(plate_number=application.plate_number)
                    vehicle.service_street = application.service_street
                    vehicle.type = application.type
                    vehicle.energy_type = application.energy_type
                    vehicle.load = application.load
                    vehicle.meet_spec = application.meet_spec
                    vehicle.save()
                else:
                    pass
                # 生成历史记录
                VehicleHistory.objects.create(
                    company=application.company,
                    plate_number=application.plate_number,
                    service_street=application.service_street,
                    type=application.type,
                    energy_type=application.energy_type,
                    load=application.load,
                    meet_spec=application.meet_spec,
                    change_type=application.change_type,
                )
            application.save()
    except VehicleApplication.DoesNotExist:
        raise HttpError(404, "审批不存在或已审批完成")
    except Vehicle.DoesNotExist:
        raise HttpError(404, "车辆不存在或已被删除")
    except IntegrityError:
        raise HttpError(409, "车辆已存在")

    return application
