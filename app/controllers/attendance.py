from datetime import date, time

from django.core.paginator import Paginator
from ninja import Query, Router

from app.models.attendance import Attendance, WorkingTime
from app.schemas import Pagination
from app.schemas.attendance import AttendanceOut, WorkingTimeOut
from infra.authentication import AuthToken, TerminalAuth

router = Router(tags=["考勤管理"])


@router.get("", response=Pagination[AttendanceOut])
def list_attendance(
    request,
    start_time: date = None,
    end_time: date = None,
    staff_id: int = None,
    toilet_id: int = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """查看考勤"""

    queryset = Attendance.objects.select_related("staff").order_by("-day", "staff_id")
    if start_time:
        queryset = queryset.filter(day__gte=start_time)
    if end_time:
        queryset = queryset.filter(day__lte=end_time)
    if staff_id is not None:
        queryset = queryset.filter(staff_id=staff_id)
    if toilet_id is not None:
        queryset = queryset.filter(staff__manage_toilet_id=toilet_id)
    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.put("working-time", response=WorkingTimeOut)
def change_working_time(request, start: time, end: time):
    """ "修改工作时间"""

    working_time = WorkingTime.get_working_time()
    working_time.start = start
    working_time.end = end
    working_time.save()
    return working_time


@router.get("working-time", response=WorkingTimeOut, auth=[AuthToken(), TerminalAuth()])
def get_working_time(request):
    working_time = WorkingTime.get_working_time()
    return working_time
