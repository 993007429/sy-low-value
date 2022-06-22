from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from ninja import Query, Router
from ninja.errors import HttpError
from pydantic import PositiveInt

from app.models import Organization, Toilet
from app.models.staff import GenderEnum, Staff
from app.schemas import Pagination
from app.schemas.staff import StaffIn, StaffOut

router = Router(tags=["人员档案"])


@router.post("", response={201: StaffOut})
def create_staff(request, staff_in: StaffIn):
    """新增工作人员"""

    pre_check(staff_in, None)
    staff = Staff.objects.create(**staff_in.dict())
    return staff


@router.get("", response=Pagination[StaffOut])
def list_staffs(
    request,
    phone: str = None,
    job_number: str = Query(None, description="工号"),
    work_card: str = Query(None, description="工牌"),
    toilet_id: int = None,
    name: str = None,
    organization_id: int = Query(None, description="管理单位"),
    gender: GenderEnum = Query(None, description="性别"),
    page: PositiveInt = Query(default=1),
    page_size: int = Query(default=20, le=100, ge=0),
):
    """工作人员列表"""

    queryset = Staff.objects.all().select_related("organization").order_by("-created_at")
    if phone:
        queryset = queryset.filter(phone=phone)
    if job_number:
        queryset = queryset.filter(job_number=job_number)
    if work_card:
        queryset = queryset.filter(work_card=work_card)
    if name:
        queryset = queryset.filter(name__contains=name)
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    if gender:
        queryset = queryset.filter(gender=gender)
    if toilet_id:
        queryset = queryset.filter(manage_toilet_id=toilet_id)
    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.delete("/{id_}", response={204: None})
def delete_staff(request, id_: int):
    """删除工作人员"""

    try:
        staff = Staff.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(status_code=404, message="员工不存在或已被删除")
    staff.delete()
    return None


@router.put("/{id_}", response=StaffOut)
def update_staff(request, id_: int, staff_in: StaffIn):
    """更新工作人员"""

    try:
        staff = Staff.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(status_code=404, message="员工不存在或已被删除")
    pre_check(staff_in, id_)
    for attr, value in staff_in.dict().items():
        setattr(staff, attr, value)
    staff.save()
    return staff


def pre_check(staff_in: StaffIn, id_: int = None):
    if staff_in.job_number:
        qs = Staff.objects.filter(job_number=staff_in.job_number)
        if id_ is not None:  # update
            qs = qs.exclude(pk=id_)
        if qs.exists():
            raise HttpError(status_code=409, message="工号已存在")
    if staff_in.work_card:
        qs = Staff.objects.filter(work_card=staff_in.work_card)
        if id_ is not None:  # update
            qs = qs.exclude(pk=id_)
        if qs.exists():
            raise HttpError(status_code=409, message="工牌已存在")

    if staff_in.organization_id is not None and not Organization.objects.filter(pk=staff_in.organization_id).exists():
        raise HttpError(status_code=404, message="管理单位不存在")
    if staff_in.manage_toilet_id is not None and not Toilet.objects.filter(pk=staff_in.manage_toilet_id).exists():
        raise HttpError(status_code=404, message="公厕不存在")
