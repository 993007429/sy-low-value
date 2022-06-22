from collections import Counter
from math import pi
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, QuerySet
from django.db.models.functions import ACos, Cos, Sin
from ninja import Query, Router
from ninja.errors import HttpError

from app.depends import (
    get_air_quality_service,
    get_passenger_volume_service,
    get_toilet_seat_service,
    get_water_meter_service,
)
from app.models import Sensor, Staff, Toilet
from app.models.toilet import StatusEnum
from app.schemas import Pagination
from app.schemas.toilet import ToiletIn, ToiletOut, ToiletRealtimeInfoOut, ToiletUpdate

router = Router(tags=["公厕"])


@router.post("", response={201: ToiletOut})
def create_toilet(request, toilet_in: ToiletIn):
    if Toilet.objects.filter(name=toilet_in.name).exists():
        raise HttpError(409, "公厕名已存在")
    if toilet_in.code and Toilet.objects.filter(code=toilet_in.code).exists():
        raise HttpError(409, "编号已存在")
    if toilet_in.manager_id and not Staff.objects.filter(pk=toilet_in.manager_id).exists():
        raise HttpError(404, "员工不存在")
    if Toilet.objects.filter(terminal_id=toilet_in.terminal_id).exists():
        t = Toilet.objects.all().order_by("-terminal_id").first()
        raise HttpError(409, f"终端号已存在, 当前最大编号为{t.terminal_id}")
    sensor_ids = {s.sensor_id for s in toilet_in.sensors}
    if len(sensor_ids) < len(toilet_in.sensors):
        duplicates = [
            sensor_id for sensor_id, count in Counter([s.sensor_id for s in toilet_in.sensors]).items() if count > 1
        ]
        raise HttpError(409, f"传感器编号 {duplicates} 重复")

    if Sensor.objects.filter(sensor_id__in=sensor_ids):
        s = Sensor.objects.all().order_by("-sensor_id").first()
        raise HttpError(409, f"传感器编号已存在, 当前最大编号为{s.sensor_id}")

    data = toilet_in.dict()
    sensors_in: List[dict] = data.pop("sensors")
    with transaction.atomic():
        toilet = Toilet.objects.create(**data)
        sensors = [Sensor(**s, toilet=toilet) for s in sensors_in]
        Sensor.objects.bulk_create(sensors)

    return toilet


@router.delete("/{id_}", response={204: None})
def delete_toilet(request, id_: int):
    try:
        toilet = Toilet.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕不存在")
    toilet.delete()
    return None


@router.put("/{id_}", response=ToiletOut)
def update_toilet(request, id_: int, toilet_update: ToiletUpdate):
    try:
        toilet = Toilet.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕不存在")
    if Toilet.objects.exclude(pk=id_).filter(name=toilet_update.name).exists():
        raise HttpError(409, "公厕名已存在")
    if toilet_update.manager_id and not Staff.objects.filter(pk=toilet_update.manager_id).exists():
        raise HttpError(404, "员工不存在")
    if toilet_update.code and Toilet.objects.exclude(pk=id_).filter(code=toilet_update.code).exists():
        raise HttpError(409, "编号已存在")
    if Toilet.objects.exclude(pk=id_).filter(terminal_id=toilet_update.terminal_id).exists():
        t = Toilet.objects.all().order_by("-terminal_id").first()
        raise HttpError(409, f"终端号已存在, 当前最大编号为{t.terminal_id}")

    sensor_ids = {s.sensor_id for s in toilet_update.sensors if s.sensor_id}
    if len(sensor_ids) < len(toilet_update.sensors):
        duplicates = [
            sensor_id for sensor_id, count in Counter([s.sensor_id for s in toilet_update.sensors]).items() if count > 1
        ]
        raise HttpError(409, f"传感器编号 {duplicates} 重复")
    if Sensor.objects.exclude(toilet_id=id_).filter(sensor_id__in=sensor_ids):
        s = Sensor.objects.all().order_by("-sensor_id").first()
        raise HttpError(409, f"传感器编号已存在, 当前最大编号为{s.sensor_id}")

    data = toilet_update.dict()
    sensors_in: List[dict] = data.pop("sensors")
    with transaction.atomic():
        for attr, value in data.items():
            setattr(toilet, attr, value)
        toilet.save()
        # 删除传感器
        existed_sensors = toilet.sensors
        to_be_deleted = {s.pk for s in existed_sensors if s.id not in sensor_ids}
        Sensor.objects.filter(pk__in=to_be_deleted).delete()
        for s in sensors_in:
            sensor = Sensor(**s, toilet=toilet)
            if sensor.pk and sensor not in existed_sensors:  # 不是当前当前公厕的传感器不能更新
                continue
            sensor.save()  # 新增或者更新

    return toilet


@router.get("", response=Pagination[ToiletOut])
def list_toilets(
    request,
    management_id: int = None,
    code: str = None,
    terminal_id: str = None,
    status: StatusEnum = None,
    name: str = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, le=100),
    longitude: float = Query(default=0),
    latitude: float = Query(default=0),
):
    queryset: QuerySet = Toilet.objects.all().order_by("-created_at")
    if all([longitude, latitude]):
        queryset: QuerySet = Toilet.objects.annotate(
            distance=ACos(
                Sin((latitude * pi) / 180) * Sin((F("latitude") * pi) / 180)
                + Cos((latitude * pi) / 180)
                * Cos((F("latitude") * pi) / 180)
                * Cos((longitude * pi) / 180 - F("longitude") * pi / 180)
            )
            * 6380
            * 1000
        ).order_by("distance")

    queryset = queryset.prefetch_related("sensor_set", "management", "toilet_type", "manager")

    if management_id:
        queryset = queryset.filter(management_id=management_id)
    if code:
        queryset = queryset.filter(code=code)
    if terminal_id:
        queryset = queryset.filter(terminal_id=terminal_id)
    if status:
        queryset = queryset.filter(status=status)
    if name:
        queryset = queryset.filter(name__contains=name)
    paginator = Paginator(object_list=queryset, per_page=page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.get("/{id_}", response=ToiletOut)
def get_toilet(request, id_: int):
    try:
        toilet = Toilet.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕不存在")
    return toilet


@router.get("/bulk/realtime-info", response=List[ToiletRealtimeInfoOut])
def bulk_get_toilet_realtime_info(request):
    """批量获取公厕传感器实时信息"""
    air_quality_service = get_air_quality_service()
    water_meter_service = get_water_meter_service()
    passenger_volume_service = get_passenger_volume_service()
    toilet_seat_service = get_toilet_seat_service()

    air_quality_list = air_quality_service.bulk_get_realtime_air_quality()
    air_quality_dict = {e.terminal_id: e for e in air_quality_list}

    meter_list = water_meter_service.bulk_get_realtime_meter()
    meter_dict = {e.terminal_id: e for e in meter_list}

    passenger_volume_list = passenger_volume_service.bulk_get_realtime_volume()
    passenger_volume_dict = {e.terminal_id: e for e in passenger_volume_list}

    toilet_seat_list = toilet_seat_service.bulk_get_realtime_toilet_seats()
    toilet_seat_dict = {e.terminal_id: e for e in toilet_seat_list}

    data = []
    for toilet in Toilet.objects.all().order_by("id"):
        air_quality = air_quality_dict.get(toilet.terminal_id)
        meter = meter_dict.get(toilet.terminal_id)
        passenger_volume = passenger_volume_dict.get(toilet.terminal_id)
        toilet_seat = toilet_seat_dict.get(toilet.terminal_id)

        realtime_info = ToiletRealtimeInfoOut(
            id=toilet.pk,
            terminal_id=toilet.terminal_id,
            name=toilet.name,
            code=toilet.code,
            address=toilet.address,
            men_toilet_total=toilet.men_toilet_nums,
            women_toilet_total=toilet.women_toilet_nums,
            genderless_toilet_total=toilet.genderless_toilet_nums,
            supporting_facilities=toilet.supporting_facilities,
            photos=toilet.photos,
            camera_serial=toilet.camera_serial,
            camera_channel=toilet.camera_channel,
            **(air_quality.dict(exclude_none=True, exclude={"terminal_id"}) if air_quality else {}),
            **(meter.dict(exclude_none=True, exclude={"terminal_id"}) if meter else {}),
            **({"passenger_volume": passenger_volume.volume} if passenger_volume else {}),
            **(toilet_seat.dict(exclude_none=True, exclude={"terminal_id"}) if toilet_seat else {}),
        )
        data.append(realtime_info)

    return data


@router.get("/{id_}/realtime-info", response=ToiletRealtimeInfoOut)
def get_toilet_realtime_info(request, id_: int):
    """获取公厕传感器实时信息"""
    try:
        toilet = Toilet.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕不存在")
    air_quality_service = get_air_quality_service()
    water_meter_service = get_water_meter_service()
    passenger_volume_service = get_passenger_volume_service()
    toilet_seat_service = get_toilet_seat_service()

    air_quality = air_quality_service.get_realtime_air_quality(toilet.terminal_id)
    meter = water_meter_service.get_realtime_meter(toilet.terminal_id)
    passenger_volume = passenger_volume_service.get_realtime_volume(toilet.terminal_id)
    toilet_seat = toilet_seat_service.get_realtime_toilet_seats(toilet.terminal_id)

    realtime_info = ToiletRealtimeInfoOut(
        id=toilet.pk,
        terminal_id=toilet.terminal_id,
        name=toilet.name,
        code=toilet.code,
        address=toilet.address,
        men_toilet_total=toilet.men_toilet_nums,
        women_toilet_total=toilet.women_toilet_nums,
        genderless_toilet_total=toilet.genderless_toilet_nums,
        supporting_facilities=toilet.supporting_facilities,
        photos=toilet.photos,
        camera_serial=toilet.camera_serial,
        camera_channel=toilet.camera_channel,
        **(air_quality.dict(exclude_none=True, exclude={"terminal_id"}) if air_quality else {}),
        **(meter.dict(exclude_none=True, exclude={"terminal_id"}) if meter else {}),
        **({"passenger_volume": passenger_volume.volume} if passenger_volume else {}),
        **(toilet_seat.dict(exclude_none=True, exclude={"terminal_id"}) if toilet_seat else {}),
    )
    return realtime_info
