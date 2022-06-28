from django.core.paginator import Paginator
from django.db import IntegrityError
from ninja import Router, Query
from ninja.errors import HttpError

from infra.authentication import User
from infra.schemas import Pagination, Page
from recycle.models import Driver
from recycle.schemas.driver import DriverOut, DriverIn

router = Router(tags=["驾驶员"])


@router.post("", response={201: DriverOut})
def create_driver(request, data: DriverIn):
    # TODO: 公司权限
    user: User = request.auth
    try:
        driver = Driver.objects.create(company=user.companymanager.company,
                                       **data.dict())
    except IntegrityError:
        raise HttpError(409, "司机身份证或联系电话重复")
    return driver


@router.get("", response=Pagination[DriverOut])
def list_drivers(request, name: str = Query(None, title="司机姓名"), page: Page = Query(...)):
    # TODO: 公司权限
    user: User = request.auth
    queryset = Driver.objects.filter(company=user.companymanager.company).order_by("-id")
    if name:
        queryset = queryset.filter(name__contains=name)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.put("/{id_}", response=DriverOut)
def update_driver(request, id_: int, data: DriverIn):
    # TODO: 公司权限
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
def delete_driver(request, id_: str):
    # TODO: 公司用户
    user: User = request.auth
    try:
        Driver.objects.filter(company=user.companymanager.company).get(pk=id_).delete()
    except Driver.DoesNotExist:
        raise HttpError(404, "司机不存在或已被删除")
