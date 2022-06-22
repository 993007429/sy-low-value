from datetime import timedelta

from django.core.paginator import Paginator
from ninja import Query, Router

from app.models.sensors import Sensor, SensorType
from app.schemas import Pagination
from app.schemas.sensor import SensorOut
from infra.const import ONLINE_TIMEDELTA
from infra.utils import now_tz_aware

router = Router(tags=["传感器"])


@router.get("", response=Pagination[SensorOut])
def list_sensors(
    request,
    terminal_id: str = None,
    toilet_name: str = None,
    management_id: str = None,
    is_online: bool = None,
    sensor_type: SensorType = None,
    sensor_id: str = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    queryset = Sensor.objects.all().select_related("toilet", "toilet__management").order_by("id")
    if terminal_id:
        queryset = queryset.filter(toilet__terminal_id=terminal_id)
    if toilet_name:
        queryset = queryset.filter(toilet__name__contains=toilet_name)
    if management_id:
        queryset = queryset.filter(toilet__management_id=management_id)
    if sensor_type:
        queryset = queryset.filter(sensor_type=sensor_type)
    if sensor_id:
        queryset = queryset.filter(sensor_id=sensor_id)
    if is_online is not None:
        limit = now_tz_aware() - timedelta(minutes=ONLINE_TIMEDELTA)
        if is_online:
            queryset = queryset.filter(last_communication_time__gte=limit)
        else:
            queryset = queryset.filter(last_communication_time__lt=limit)

    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}
