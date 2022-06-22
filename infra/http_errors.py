from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError


class AuthenticationFailed(HttpError):
    status_code = 401
    default_detail = _("Incorrect authentication credentials.")
    default_code = "authentication_failed"


class NotAuthenticated(HttpError):
    status_code = 401
    default_detail = _("Authentication credentials were not provided.")
    default_code = "not_authenticated"


class PermissionDenied(HttpError):
    status_code = 403
    default_detail = _("You do not have permission to perform this action.")
    default_code = "permission_denied"


class NotFound(HttpError):
    status_code = 404
    default_detail = _("Not found.")
    default_code = "not_found"
