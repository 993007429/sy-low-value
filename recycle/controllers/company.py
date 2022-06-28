from typing import List

from django.core.paginator import Paginator
from django.db.models import Count
from ninja import Query, Router

from infra.schemas import Page, Pagination
from recycle.models import Company
from recycle.schemas.company import CompanyOut, CompanyDropdownOut

router = Router(tags=["收运公司"])


@router.get("/dropdown", response=List[CompanyDropdownOut])
def list_all_companies(request):
    queryset = Company.objects.values("id", "name")
    return queryset


@router.get("", response=Pagination[CompanyOut])
def list_companies(
        request,
        name: str = Query(None, title="公司名称"),
        uniform_social_credit_code: str = Query(None, title="统一社会信用代码"),
        page: Page = Query(...),
):
    # TODO：限制权限为再生资源平台管理员
    queryset = Company.objects.annotate(vehicle_count=Count("vehicle")).prefetch_related("manager").order_by("-id")
    if name:
        queryset = queryset.filter(name__contains=name)
    if uniform_social_credit_code:
        queryset = queryset.filter(uniform_social_credit_code=uniform_social_credit_code)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}
