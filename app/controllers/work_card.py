from django.db import transaction
from ninja import Router

from app.models import Attendance, Staff
from app.models.sensors import Sensor, WorkCardScan
from app.schemas.work_card import WorkCardIn, WorkCardOut
from infra.authentication import terminal_auth
from infra.utils import now_tz_aware

router = Router(tags=["工牌检测"])


@router.post("", response={201: WorkCardOut}, auth=terminal_auth)
def create_work_card(request, data: WorkCardIn):
    """工牌检测传感器数据上传"""

    WorkCardScan.objects.create(work_card=data.work_card)
    # 更新传感器最后通信时间
    Sensor.update_last_communication_time(data.sensor_id)
    # 更新对应考勤
    now = now_tz_aware()
    staff = Staff.objects.filter(work_card=data.work_card).first()
    with transaction.atomic():
        attendance = Attendance.objects.filter(day=now.date(), staff=staff).select_for_update().first()
        if staff and attendance:
            # 上班取第一次打卡，下班取最后一次打卡
            noon = now.replace(hour=12, minute=0, second=0, microsecond=0)
            if now < noon:
                if not attendance.clock_in:
                    attendance.clock_in = now
                    attendance.save()
            else:
                attendance.clock_out = now
                attendance.save()

    return WorkCardOut(timestamp=now)
