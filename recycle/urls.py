import logging

from django.conf import settings
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI
from ninja.errors import ValidationError

from infra.authentication import AuthToken
from infra.renderers import JSONRenderer

from .controllers.company import router as company_router
from .controllers.company_application import router as company_application_router
from .controllers.driver import router as driver_router
from .controllers.event import router as event_router
from .controllers.inbound import router as inbound_router
from .controllers.inbound_statistics import router as inbound_statistics_router
from .controllers.monitor import router as monitor_router
from .controllers.notification import router as notification_router
from .controllers.outbound import router as outbound_router
from .controllers.region import router as region_router
from .controllers.statistics import router as statistics_router
from .controllers.token import router as token_router
from .controllers.track import router as track_router
from .controllers.transfer_station import router as transfer_station_router
from .controllers.vehicle import router as vehicle_router
from .controllers.vehicle_application import router as vehicle_application_router
from .controllers.vehicle_draft import router as vehicle_draft_router
from .controllers.vehicle_history import router as vehicle_history_router

logger = logging.getLogger(__name__)

api = NinjaAPI(auth=AuthToken(), renderer=JSONRenderer())
# api = NinjaAPI(renderer=JSONRenderer())

if not settings.DEBUG:
    api.docs_url = None


@api.exception_handler(ValidationError)
def validation_errors(request: HttpRequest, exc: ValidationError):
    print(request.body.decode())
    print(exc.errors)
    return api.create_response(request, {"detail": exc.errors}, status=422)


api.add_router("/login", token_router)
api.add_router("/region", region_router)
api.add_router("/company", company_router)
api.add_router("/company-application", company_application_router)
api.add_router("/vehicle-drft", vehicle_draft_router)
api.add_router("/vehicle-application", vehicle_application_router)
api.add_router("/vehicle", vehicle_router)
api.add_router("/vehicle-history", vehicle_history_router)
api.add_router("/driver", driver_router)

api.add_router("/transfer-station", transfer_station_router)
api.add_router("/inbound", inbound_router)
api.add_router("/outbound", outbound_router)
api.add_router("/inbound-statistics", inbound_statistics_router)
api.add_router("/statistics", statistics_router)
api.add_router("/track", track_router)
api.add_router("/monitor", monitor_router)
api.add_router("/event", event_router)
api.add_router("/notification", notification_router)

urlpatterns = [
    path("", api.urls),
]
