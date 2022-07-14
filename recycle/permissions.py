from django.http import HttpRequest

from infra.permissions import BasePermission
from recycle.models import CompanyManager, PlatformManager


class IsPlatformManager(BasePermission):
    """再生资源平台用户"""

    def has_permission(self, request: HttpRequest, view_func):
        return PlatformManager.objects.filter(user=request.auth).exists()


class IsCompanyManager(BasePermission):
    """清运公司平台用户"""

    def has_permission(self, request: HttpRequest, view_func):
        return CompanyManager.objects.filter(user=request.auth).exists()


class IsStreetManager(BasePermission):
    """再生资源平台街道用户"""

    def has_permission(self, request: HttpRequest, view_func):
        return PlatformManager.objects.filter(user=request.auth, role=PlatformManager.STREET).exists()
