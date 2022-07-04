import logging
import time

import jwt
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from jwt import DecodeError
from ninja.errors import HttpError
from ninja.security import HttpBearer
from pydantic import BaseModel, Field

User = get_user_model()
logger = logging.getLogger("django")


class AuthToken(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, "HS256")
            userid = payload["userid"]
            user = User.objects.get(pk=userid)
            user.token = token
            return user
        except (jwt.ExpiredSignatureError, DecodeError, ObjectDoesNotExist):
            return None


def get_tokens_for_user(user: User):
    expired_at = int(time.time()) + settings.JWT_EXPIRE
    payload = {"userid": user.pk, "exp": expired_at}
    return jwt.encode(payload, settings.SECRET_KEY, "HS256")


class LjflUser(BaseModel):
    """
    精细化管理平台用户
    """

    role: str
    relation_id: str
    username: str
    city_code: str = Field(None, alias="city_coding")
    city_name: str = Field(None, alias="city_name")
    street_code: str = Field(None, alias="street_coding")
    street_name: str = Field(None, alias="street_name")
    community_code: str = Field(None, alias="comm_coding")
    community_name: str = Field(None, alias="comm_name")
    token: str


class LjflToken(HttpBearer):
    """垃圾分类精细化管理平台用户认证，用于让市级区级系统可以查看本系统信息"""

    def authenticate(self, request, token):
        url = settings.AUTH_SERVER_URL + f"/oauth/manager?token={token}&appid=117998218"
        try:
            response = requests.get(url)
            if response.ok:
                result = response.json()
                user = result["data"]["manager"]
                user["token"] = token
                return LjflUser(**user)
        except Exception:
            logger.exception(f"访问认证服务失败. {url}")
            raise HttpError(503, "认证服务不可用")
