import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from ninja import Router
from ninja.errors import HttpError

from app.models import User
from app.models.user import WeChatUser
from app.schemas.token import Token
from app.schemas.user import WechatLogin, WechatSession, WechatUserUpdate, WechatUserVo
from infra.authentication import get_tokens_for_user

router = Router(tags=["微信"])


def get_wechat_login_url(appid: str, secret: str, code: str) -> str:
    return (
        "https://api.weixin.qq.com/sns/jscode2session"
        f"?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"
    )


@router.post("/login", auth=None, response={201: Token})
def wechat_login(request, wechat_login: WechatLogin):
    login_url = get_wechat_login_url(settings.MINI_APP_ID, settings.MINI_APP_SECRET, wechat_login.code)
    response = requests.get(login_url)
    if not response.ok:
        raise HttpError(503, "请求微信登陆授权返回错误")
    wechat_session = WechatSession(**response.json())
    if wechat_session.errcode:
        raise HttpError(400, wechat_session.errmsg)
    openid = wechat_session.openid

    user, created = User.objects.get_or_create(username=openid)
    if created:
        WeChatUser.objects.create(
            user=user,
            openid=openid,
            unionid=wechat_session.unionid,
            session_key=wechat_session.session_key,
        )

    user.last_login = timezone.now()
    user.save()
    token = get_tokens_for_user(user)

    return Token(username=user.username, nickname=user.nickname, phone=user.phone, token=token, user_id=user.pk)


@router.put("/user", response={200: WechatUserVo})
def update_wechat_user(request, wechat_update: WechatUserUpdate):
    try:
        wechat_user = WeChatUser.objects.get(user=request.auth)
    except ObjectDoesNotExist:
        raise HttpError(404, "小程序用户不存在")

    wechat_user.nickname = wechat_update.nickname
    wechat_user.avatar = wechat_update.avatar
    wechat_user.gender = wechat_update.gender
    wechat_user.country = wechat_update.country
    wechat_user.province = wechat_update.province
    wechat_user.city = wechat_update.city

    with transaction.atomic():
        wechat_user.save()
        wechat_user.user.nickname = wechat_update.nickname
        wechat_user.user.save()

    return wechat_user
