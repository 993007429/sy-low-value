import functools
from typing import List, Type

from django.http import HttpRequest

from infra.permissions import BasePermission, check_permissions


def permission_required(permission_classes: List[Type[BasePermission]]):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # django-ninja view func第一个参数固定为 request
            request: HttpRequest = args[0]
            permissions = [permission() for permission in permission_classes]
            check_permissions(request, permissions, func)
            return func(*args, **kwargs)

        return wrapper

    return decorate
