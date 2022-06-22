from datetime import date, datetime, time

from ninja import Schema
from pydantic import Field


class AttendanceOut(Schema):
    staff_id: int
    staff_name: str
    day: date = Field(..., title="考勤日期")
    work_card: str = Field(None, title="工牌", alias="staff.work_card")
    toilet_name: str = Field(None, title="公厕")
    start_working_time: time = Field(..., title="规定上班时间")
    clock_in: datetime = Field(None, title="上班打卡时间, 没值则为未打卡")
    quiting_time: time = Field(..., title="规定下班时间")
    clock_out: datetime = Field(None, title="下班打卡时间, 没值则为未打卡")


class WorkingTimeOut(Schema):
    start: time
    end: time
