from ninja import Router

from recycle.schemas.company import CompanyIn

router = Router(tags=["收运公司"])


@router.post("")
def create_company(request, company_in: CompanyIn):
    pass
