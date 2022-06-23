import logging
import time
from typing import Any, Optional

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import Signer
from django.http import HttpRequest
from jwt import DecodeError
from ninja.compatibility import get_headers
from ninja.errors import HttpError
from ninja.security import HttpBearer
from ninja.security.http import HttpAuthBase

from recycle.models import Toilet
from recycle.models.openapi import Agent

User = get_user_model()
logger = logging.getLogger("django")

write_methods = ("POST", "PUT", "PATCH", "DELETE")


class AuthToken(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, "HS256")
        except jwt.ExpiredSignatureError:
            raise HttpError(status_code=401, message="token expired")
        except DecodeError:
            raise HttpError(status_code=401, message="token invalid")
        userid = payload["userid"]
        try:
            user = User.objects.get(pk=userid)
            user.token = token
            self.check_permissions(request, user)
            return user
        except ObjectDoesNotExist:
            raise HttpError(status_code=404, message="user not found")

    @staticmethod
    def check_permissions(request, user: User):
        if request.method in write_methods and user.username in settings.READONLY_USERS:
            raise HttpError(status_code=403, message="权限不足")


def get_tokens_for_user(user: User):
    expired_at = int(time.time()) + settings.JWT_EXPIRE
    payload = {"userid": user.pk, "exp": expired_at}
    return jwt.encode(payload, settings.SECRET_KEY, "HS256")


def get_tokens_for_agent(agent_id: str):
    signer = Signer()
    payload = {"agent": agent_id, "ts": int(time.time())}
    return signer.sign_object(payload)


class TerminalAuth(HttpAuthBase):
    openapi_scheme: str = "bearer"
    header: str = "X-Terminal-Sign"

    def __call__(self, request: HttpRequest) -> Optional[Any]:
        headers = get_headers(request)
        auth_value = headers.get(self.header)
        if not auth_value:
            return None
        return self.authenticate(request, auth_value)

    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        signer = Signer()
        try:
            terminal_id = signer.unsign(token)
        except signing.BadSignature:
            raise HttpError(status_code=401, message="invalid signature")
        try:
            toilet = Toilet.objects.get(terminal_id=terminal_id)
        except ObjectDoesNotExist:
            raise HttpError(404, "公厕不存在")
        return toilet


class AgentAuth(HttpBearer):
    """认证受信任的三方系统"""

    def authenticate(self, request, token):
        signer = Signer()
        try:
            payload = signer.unsign_object(token)
        except signing.BadSignature:
            raise HttpError(status_code=401, message="invalid signature")
        try:
            agent = Agent.objects.select_related("authorizer").get(agent_id=payload["agent"], secret=token)
        except ObjectDoesNotExist:
            raise HttpError(status_code=401, message="invalid signature")
        return agent


terminal_auth = TerminalAuth()

agent_auth = AgentAuth()
