from django.core.paginator import Paginator
from django.db import IntegrityError
from ninja import Query, Router
from ninja.errors import HttpError

from infra.authentication import User
from infra.decorators import permission_required
from infra.schemas import Page, Pagination
from recycle.models import Driver
from recycle.permissions import IsCompanyManager
from recycle.schemas.driver import DriverIn, DriverOut

router = Router(tags=["驾驶员"])


@router.post("", response={201: DriverOut})
@permission_required([IsCompanyManager])
def create_driver(request, data: DriverIn):
    user: User = request.auth
    try:
        driver = Driver.objects.create(company=user.companymanager.company, **data.dict())
    except IntegrityError:
        raise HttpError(409, "司机身份证或联系电话重复")
    return driver


@router.get("", response=Pagination[DriverOut])
@permission_required([IsCompanyManager])
def list_drivers(request, name: str = Query(None, title="司机姓名"), page: Page = Query(...)):
    user: User = request.auth
    queryset = Driver.objects.filter(company=user.companymanager.company).order_by("-id")
    if name:
        queryset = queryset.filter(name__contains=name)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.put("/{id_}", response=DriverOut)
@permission_required([IsCompanyManager])
def update_driver(request, id_: int, data: DriverIn):
    user: User = request.auth
    try:
        driver = Driver.objects.get(company=user.companymanager.company, pk=id_)
        for attr, value in data.dict().items():
            setattr(driver, attr, value)
        driver.save()
    except Driver.DoesNotExist:
        raise HttpError(404, "司机不存在")
    except IntegrityError:
        raise HttpError(409, "司机身份证或联系电话重复")
    return driver


@router.delete("/{id_}", response={204: None})
@permission_required([IsCompanyManager])
def delete_driver(request, id_: str):
    user: User = request.auth
    try:
        Driver.objects.filter(company=user.companymanager.company).get(pk=id_).delete()
    except Driver.DoesNotExist:
        raise HttpError(404, "司机不存在或已被删除")
