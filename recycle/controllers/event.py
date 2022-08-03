from datetime import datetime
from typing import List

from ninja import Query, Router
from ninja.pagination import paginate

from recycle.models.event import Event, EventType
from recycle.schemas.event import EventOut

router = Router(tags=["实时预警"])


@router.get("", response=List[EventOut], auth=None)
@paginate
def list_events(
    request,
    plate_number: str = Query(None, description="车牌号"),
    start_time: datetime = Query(None, description="开始时间"),
    end_time: datetime = Query(None, description="结束时间"),
    event_type: EventType = Query(None, description="事件类型"),
):
    queryset = Event.objects.all()
    if plate_number:
        queryset = queryset.filter(plate_number=plate_number)
    if start_time:
        queryset = queryset.filter(started_at__gte=start_time)
    if end_time:
        queryset = queryset.filter(started_at__lte=end_time)
    if event_type:
        queryset = queryset.filter(type=event_type)
    return queryset
