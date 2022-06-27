from django.contrib.auth import authenticate
from ninja import Router
from ninja.errors import HttpError

from infra.authentication import get_tokens_for_user
from recycle.schemas.token import Login, Token

router = Router(tags=["Token"])


@router.post("", auth=None, response={201: Token})
def get_token(request, login: Login):
    user = authenticate(**login.dict())
    if not user:
        raise HttpError(404, "密码错误或帐号不存在")
    token = get_tokens_for_user(user)
    return Token(username=user.username, name=user.first_name, token=token, user_id=user.pk)
