from django.core.paginator import Paginator
from ninja import Query, Router

from infra.schemas import Page, Pagination
from recycle.models import PlatformManager, ServiceStreetModification, User
from recycle.schemas.notification import ServiceStreetModificationOut

router = Router(tags=["通知"])


@router.get("/service-street-modification", response=Pagination[ServiceStreetModificationOut])
def get_unread_service_street_modifications(
    request,
    page: Page = Query(...),
):
    """查询未读的服务街道变更通知"""

    street_id = None
    if isinstance(request.auth, User) and (
        pm := PlatformManager.objects.filter(user=request.auth, role=PlatformManager.STREET).first()
    ):
        street_id = pm.region_id

    queryset = ServiceStreetModification.objects.filter(source_street__code=street_id, read=False).select_related(
        "source_street", "target_street"
    )
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    response = {"count": paginator.count, "results": list(p.object_list)}
    ServiceStreetModification.objects.filter(source_street__code=street_id).update(read=True)
    return response
