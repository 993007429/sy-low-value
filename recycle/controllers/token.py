from django.contrib.auth import authenticate
from ninja import Router
from ninja.errors import HttpError

from infra.authentication import get_tokens_for_user
from recycle.models import CompanyManager, HazardousWasteCompany, PlatformManager, User
from recycle.schemas.companytoken import CompanyToken, HazardousWasteCompanyToken, Login, PlatformToken

router = Router(tags=["Token"])

MSG_PASSWORD_NOT_MATCH = "密码错误或帐号不存在"


@router.post("platform", auth=None, response={201: PlatformToken})
def get_platform_token(request, login: Login):
    """再生资源平台登录"""

    user: User = authenticate(**login.dict())
    platform_user = PlatformManager.objects.filter(user=user).first()
    if not (user and platform_user):
        raise HttpError(404, MSG_PASSWORD_NOT_MATCH)
    token = get_tokens_for_user(user)
    return PlatformToken(
        username=user.username, name=user.first_name, token=token, user_id=user.pk, role=platform_user.role
    )


@router.post("company", auth=None, response={201: CompanyToken})
def get_company_token(request, login: Login):
    """清运公司端登录"""

    user = authenticate(**login.dict())
    if not user:
        raise HttpError(404, MSG_PASSWORD_NOT_MATCH)
    company_user = CompanyManager.objects.filter(user=user).prefetch_related("company", "company__stations").first()
    if not company_user:
        raise HttpError(404, MSG_PASSWORD_NOT_MATCH)
    token = get_tokens_for_user(user)
    return CompanyToken(
        username=user.username,
        name=user.first_name,
        token=token,
        user_id=user.pk,
        social_credit_code=company_user.company.uniform_social_credit_code,
        has_transfer_station=company_user.company.stations.exists(),
    )


@router.post("hazardous_waste_company", auth=None, response={201: HazardousWasteCompanyToken})
def get_hazardous_company_token(request, login: Login):
    """有害垃圾公司登录"""

    user: User = authenticate(**login.dict())
    company = HazardousWasteCompany.objects.filter(user=user).first()
    if not (user and company):
        raise HttpError(404, MSG_PASSWORD_NOT_MATCH)
    token = get_tokens_for_user(user)
    return HazardousWasteCompanyToken(username=user.username, name=user.first_name, token=token, user_id=user.pk)
