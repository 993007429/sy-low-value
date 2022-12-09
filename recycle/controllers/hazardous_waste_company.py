from typing import List

from django.db import IntegrityError
from ninja import Query, Router
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate

from infra.authentication import User
from infra.decorators import permission_required
from recycle.models import HazardousWasteCompany
from recycle.permissions import IsPlatformManager
from recycle.schemas.hazardous_waste_company import HazardousWasteCompanyIn, HazardousWasteCompanyOut

router = Router(tags=["有害垃圾收运公司"])


@router.get("", response=List[HazardousWasteCompanyOut])
@paginate(PageNumberPagination, page_size=20)
@permission_required([IsPlatformManager])
def list_companies(
    request,
    name: str = Query(None, description="公司名称"),
    username: str = Query(None, description="登录帐号"),
):
    queryset = HazardousWasteCompany.objects.select_related("user").order_by("-id")
    if name:
        queryset = queryset.filter(name__contains=name)
    if username:
        queryset = queryset.filter(user__username__contains=username)
    return queryset


@router.post("", response=HazardousWasteCompanyOut)
@permission_required([IsPlatformManager])
def create_company(request, data: HazardousWasteCompanyIn):
    """创建有害垃圾公司帐号"""

    try:
        user = User.objects.create_user(
            username=data.username,
            first_name=data.name,
            password=data.password,
        )
        manager = HazardousWasteCompany.objects.create(
            user=user,
            name=data.name,
            password=data.password,
        )
    except IntegrityError:
        raise HttpError(409, "帐号已存在")
    return manager
