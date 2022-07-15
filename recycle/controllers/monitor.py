from django.core.paginator import Paginator
from ninja import Query, Router

from infra.schemas import Page, Pagination
from recycle.models import Monitor
from recycle.schemas.monitor import MonitorOut

router = Router(tags=["设施监控"])


@router.get("", response=Pagination[MonitorOut])
def list_monitors(request, name: str = Query(None, title="中转站名称"), page: Page = Query(...)):
    queryset = Monitor.objects.select_related("station", "station__street", "station__community")
    if name:
        queryset = queryset.filter(station__name=name)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}
