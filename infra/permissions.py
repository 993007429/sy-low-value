from typing import List

from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError


class BasePermission:
    def has_permission(self, request: HttpRequest, view_func):
        return True


def check_permissions(request: HttpRequest, permissions: List[BasePermission], view_func):
    for permission in permissions:
        if not permission.has_permission(request, view_func):
            code = getattr(permission, "code", 403)
            message = getattr(permission, "message", _("You do not have permission to perform this action."))
            raise HttpError(code, message)
