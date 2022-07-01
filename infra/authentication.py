import logging
import time

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from jwt import DecodeError
from ninja.errors import HttpError
from ninja.security import HttpBearer

User = get_user_model()
logger = logging.getLogger("django")


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
            return user
        except ObjectDoesNotExist:
            raise HttpError(status_code=401, message="user not found")


def get_tokens_for_user(user: User):
    expired_at = int(time.time()) + settings.JWT_EXPIRE
    payload = {"userid": user.pk, "exp": expired_at}
    return jwt.encode(payload, settings.SECRET_KEY, "HS256")
