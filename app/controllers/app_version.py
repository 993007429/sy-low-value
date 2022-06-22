from typing import List

from ninja import Router

from app.models import Toilet
from app.models.terminal import AppVersion
from app.schemas.terminal import AppVersionIn, AppVersionOut
from infra.authentication import terminal_auth

router = Router(tags=["终端软件版本"])


@router.post("", response={201: AppVersionOut}, auth=terminal_auth)
def post_terminal_app_version(request, data: AppVersionIn):
    toilet: Toilet = request.auth
    obj, _ = AppVersion.objects.update_or_create(terminal_id=toilet.terminal_id, defaults=data.dict())
    return obj


@router.get("", response=List[AppVersionOut])
def list_terminal_app_versions(request):
    return AppVersion.objects.all()
