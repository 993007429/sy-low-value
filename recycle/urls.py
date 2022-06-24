import logging

from django.conf import settings
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI
from ninja.errors import ValidationError

# from infra.authentication import AuthToken
from infra.renderers import JSONRenderer
from .controllers.company import router as company_router
from .controllers.transfer_station import router as transfer_station_router

logger = logging.getLogger(__name__)

# api = NinjaAPI(auth=AuthToken(), renderer=JSONRenderer())
api = NinjaAPI(renderer=JSONRenderer())

if not settings.DEBUG:
    api.docs_url = None


@api.exception_handler(ValidationError)
def validation_errors(request: HttpRequest, exc: ValidationError):
    print(request.body.decode())
    print(exc.errors)
    return api.create_response(request, {"detail": exc.errors}, status=422)


api.add_router("/company", company_router)
api.add_router("/transfer-station", transfer_station_router)

urlpatterns = [
    path("", api.urls),
]
