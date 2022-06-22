import logging

from django.conf import settings
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI
from ninja.errors import ValidationError

from app.controllers.air_quality import router as air_quality_router
from app.controllers.ammeter import router as ammeter_router
from app.controllers.app_version import router as app_version_router
from app.controllers.attendance import router as attendance_router
from app.controllers.h2s import router as h2s_router
from app.controllers.nh3 import router as nh3_router
from app.controllers.openapi import router as openapi_router
from app.controllers.organization import router as organization_router
from app.controllers.passenger_volume import router as passenger_volume_router
from app.controllers.sensor import router as sensor_router
from app.controllers.staff import router as staff_router
from app.controllers.toilet import router as toilet_router
from app.controllers.toilet_comment import router as toilet_comment_router
from app.controllers.toilet_seat import router as toilet_seat_controller
from app.controllers.token import router as token_router
from app.controllers.toliet_type import router as toilet_type_router
from app.controllers.water_meter import router as water_meter_router
from app.controllers.wechat import router as wechat_router
from app.controllers.work_card import router as work_car_router
from infra.authentication import AuthToken
from infra.renderers import JSONRenderer

logger = logging.getLogger(__name__)

api = NinjaAPI(auth=AuthToken(), renderer=JSONRenderer())

if not settings.DEBUG:
    api.docs_url = None


@api.exception_handler(ValidationError)
def validation_errors(request: HttpRequest, exc: ValidationError):
    print(request.body.decode())
    print(exc.errors)
    return api.create_response(request, {"detail": exc.errors}, status=422)


api.add_router("/login", token_router)
api.add_router("/wechat", wechat_router)
api.add_router("/organization", organization_router)
api.add_router("/air_quality", air_quality_router)
api.add_router("/h2s", h2s_router)
api.add_router("/nh3", nh3_router)
api.add_router("/ammeter", ammeter_router)
api.add_router("/water-meter", water_meter_router)
api.add_router("/passenger-volume", passenger_volume_router)
api.add_router("/toilet_seat", toilet_seat_controller)
api.add_router("/toilet-type", toilet_type_router)
api.add_router("/toilet", toilet_router)
api.add_router("/sensor", sensor_router)
api.add_router("/toilet-comment", toilet_comment_router)
api.add_router("/staff", staff_router)
api.add_router("/attendance", attendance_router)
api.add_router("/work-card", work_car_router)
api.add_router("/open", openapi_router)
api.add_router("/app-version", app_version_router)

urlpatterns = [
    path("", api.urls),
]
