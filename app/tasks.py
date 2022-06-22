import logging
from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore

from app.models import Staff
from app.models.attendance import Attendance, WorkingTime

log = logging.getLogger(__name__)


@util.close_old_connections
def generate_daily_attendance(day: date = None):
    """生成每日考勤"""

    if not day:
        day = date.today()
    log.info(f"开始生成考勤 {day}")
    working_time = WorkingTime.get_working_time()
    assert working_time is not None
    for staff in Staff.objects.all():
        obj, created = Attendance.objects.get_or_create(
            defaults={"start_working_time": working_time.start, "quiting_time": working_time.end}, staff=staff, day=day
        )
        if created:
            log.info(f"生成考勤:{staff.name} {day}")
        else:
            log.info(f"考勤已存在:{staff.name} {day}")


scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")

scheduler.add_job(
    generate_daily_attendance,
    trigger=CronTrigger(hour=0),
    id="generate_daily_attendance",
    max_instances=1,
    replace_existing=True,
)
