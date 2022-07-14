from django.core.paginator import Paginator
from ninja import Path, Query, Router

from infra.schemas import Page, Pagination
from recycle.models import Company, VehicleHistory
from recycle.schemas.vehicle_history import VehicleHistoryOut

router = Router(tags=["车辆台帐变更记录"])


@router.get("/{plate_number}", response=Pagination[VehicleHistoryOut])
def list_vehicle(
    request,
    plate_number: str = Path(..., description="车牌号"),
    page: Page = Query(...),
):
    """车辆台帐变更记录"""

    queryset = (
        VehicleHistory.objects.filter(plate_number=plate_number)
        .select_related("service_street", "company")
        .order_by("id")
    )
    # 如果是公司用户则只能查看自己公司名下的数据
    if c := Company.objects.filter(manager__user=request.auth).first():
        queryset = queryset.filter(company=c)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}
