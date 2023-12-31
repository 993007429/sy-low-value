from typing import List

from django.core.paginator import Paginator
from django.db.models import Count
from ninja import Path, Query, Router
from ninja.errors import HttpError

from infra.authentication import User
from infra.decorators import permission_required
from infra.schemas import Page, Pagination
from recycle.models import Company, CompanyManager, PlatformManager
from recycle.permissions import IsPlatformManager
from recycle.schemas.company import CompanyDropdownOut, CompanyOut

router = Router(tags=["收运公司"])


@router.get("/dropdown", response=List[CompanyDropdownOut])
def list_all_companies(request):
    queryset = Company.objects.values("id", "name")
    return queryset


@router.get("", response=Pagination[CompanyOut])
@permission_required([IsPlatformManager])
def list_companies(
    request,
    name: str = Query(None, description="公司名称"),
    uniform_social_credit_code: str = Query(None, description="统一社会信用代码"),
    page: Page = Query(...),
):
    queryset = Company.objects.annotate(vehicle_count=Count("vehicle")).prefetch_related("manager").order_by("-id")
    if name:
        queryset = queryset.filter(name__contains=name)
    if uniform_social_credit_code:
        queryset = queryset.filter(uniform_social_credit_code=uniform_social_credit_code)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.get("/{credit_code}", response=CompanyOut)
def get_company_by_credit_code(request, credit_code: str = Path(..., description="公司统一社会信用代码")):
    user: User = request.auth
    queryset = (
        Company.objects.annotate(vehicle_count=Count("vehicle"))
        .filter(uniform_social_credit_code=credit_code)
        .select_related("manager")
    )
    if PlatformManager.objects.filter(user=user).exists():
        company = queryset.first()
    elif CompanyManager.objects.filter(user=user).exists():
        company = queryset.filter(manager__user=user).first()
    else:
        raise HttpError(403, "permission denied.")
    if not company:
        raise HttpError(404, "清运公司不存在")
    return company
