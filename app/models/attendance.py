from django.db import models

from infra.db.models import BaseModel


class Attendance(BaseModel):
    """考勤"""

    staff = models.ForeignKey("Staff", on_delete=models.CASCADE)
    day = models.DateField("考勤日期")
    start_working_time = models.TimeField("上班时间")
    clock_in = models.DateTimeField("上班打卡时间", null=True, blank=True)
    quiting_time = models.TimeField("下班时间")
    clock_out = models.DateTimeField("下班打卡时间", null=True, blank=True)

    class Meta:
        unique_together = ("day", "staff_id")

    @property
    def staff_name(self):
        return self.staff.name

    @property
    def toilet_name(self):
        return self.staff.toilet_name


class WorkingTime(BaseModel):
    """工作时间"""

    start = models.TimeField("上班时间")
    end = models.TimeField("下班时间")

    @staticmethod
    def get_working_time() -> "WorkingTime":
        obj = WorkingTime.objects.first()
        assert obj is not None
        return obj
