from django.contrib.auth import authenticate
from ninja import Router
from ninja.errors import HttpError

from infra.authentication import get_tokens_for_user
from recycle.models import CompanyManager, PlatformManager, User
from recycle.schemas.companytoken import CompanyToken, Login, PlatformToken

router = Router(tags=["Token"])


@router.post("platform", auth=None, response={201: PlatformToken})
def get_platform_token(request, login: Login):
    """再生资源平台登录"""

    user: User = authenticate(**login.dict())
    if not (user and PlatformManager.objects.filter(user=user).exists()):
        raise HttpError(404, "密码错误或帐号不存在")
    token = get_tokens_for_user(user)
    return PlatformToken(username=user.username, name=user.first_name, token=token, user_id=user.pk)


@router.post("company", auth=None, response={201: CompanyToken})
def get_company_token(request, login: Login):
    """清运公司端登录"""

    user = authenticate(**login.dict())
    if not user:
        raise HttpError(404, "密码错误或帐号不存在")
    company_user = CompanyManager.objects.filter(user=user).first()
    if not company_user:
        raise HttpError(404, "密码错误或帐号不存在")
    token = get_tokens_for_user(user)
    return CompanyToken(
        username=user.username,
        name=user.first_name,
        token=token,
        user_id=user.pk,
        social_credit_code=company_user.company.uniform_social_credit_code,
    )
