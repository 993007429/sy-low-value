import json
import logging
from datetime import datetime
from typing import List

from influxdb_client.client.write_api import SYNCHRONOUS
from ninja import Query, Router
from ninja.errors import HttpError

from app.models import Toilet
from app.models.sensors import Sensor, ToiletSeat
from app.schemas import Pagination
from app.schemas.toilet_seat import ToiletSeatIn, ToiletSeatOut, ToiletSeatStatistics, ToiletSeatStatisticsOut
from infra import const
from infra.authentication import terminal_auth
from infra.db.influxdb import flux_list, flux_list_count, flux_tables_to_models, influxdb_client
from infra.utils import now_tz_aware

router = Router(tags=["厕位"])
logger = logging.getLogger("influxdb.query")


@router.post("", response={201: None}, auth=terminal_auth)
def create_toilet_seat(request, data: ToiletSeatIn):
    """厕位传感器数据上传"""

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    toilet = request.auth
    sensor_ids = {s.sensor_id for s in data.seats}
    sensors = {s.sensor_id: s for s in Sensor.objects.filter(sensor_id__in=sensor_ids)}
    toilet_seats = []
    now = now_tz_aware()
    for seat in data.seats:
        installation_location = None  # 安装位置
        seat_serial = None  # 厕位序号
        if sensor := sensors.get(seat.sensor_id):
            installation_location = sensor.installation_location
            seat_serial = sensors.get(seat.sensor_id).serial
        toilet_seat = ToiletSeat(
            toilet_name=toilet.name,
            terminal_id=data.terminal_id,
            gather_time=now,
            sensor_id=seat.sensor_id,
            installation_location=installation_location,
            seat_serial=seat_serial,
            occupied=1 if seat.occupied else 0,
        )
        toilet_seats.append(toilet_seat.to_data_point())
    write_api.write(bucket=const.INFLUXDB_BUCKET, record=toilet_seats)
    # 更新传感器最后通信时间
    Sensor.objects.filter(sensor_id__in=sensor_ids).update(last_communication_time=now)
    return None


@router.get("", response=Pagination[ToiletSeatOut])
def list_toilet_seat(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str = None,
    sensor_id: str = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """查询厕位占用上传记录"""
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")
    offset = (page - 1) * page_size
    limit = page_size
    # TODO: 参数化查询解决注入问题（参考air_quality）

    query_api = influxdb_client.query_api()
    flux = (
        f'from(bucket: "{const.INFLUXDB_BUCKET}")'
        f"|> range(start: {start_time.isoformat()}, stop: {end_time.isoformat()})"
        '|> filter(fn: (r) => r._measurement == "toilet_seat" and exists r["seat_serial"]'
        " and exists r.installation_location"
        ' and (r.installation_location == "MEN" or r.installation_location == "WOMEN" or r.installation_location == "GENDERLESS"))'  # noqa
        '|> pivot(columnKey: ["_field"], rowKey: ["_time"], valueColumn: "_value")'
    )
    if terminal_id:
        flux += f'|> filter(fn: (r) => r.terminal_id == "{terminal_id}")'
    if sensor_id:
        flux += f'|> filter(fn: (r) => r.sensor_id == "{sensor_id}")'
    flux += "|> group()"

    # 统计总条数
    count = flux_list_count(flux, query_api)
    # 查询列表
    flux = flux_list(flux, limit, offset)
    logger.debug(flux)
    tables = query_api.query(flux)

    results: ToiletSeatOut = flux_tables_to_models(tables, ToiletSeatOut)
    return {"count": count, "results": results}


@router.get("/statistics", response=Pagination[ToiletSeatStatisticsOut])
def get_toilet_seat_statistics(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str = None,
    organization_id: int = None,
    toilet_type_id: int = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, le=100),
):
    """查询厕位上传记录"""
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")
    offset = (page - 1) * page_size
    limit = page_size
    # TODO: 参数化查询解决注入问题（参考air_quality）

    toilet_queryset = Toilet.objects.all().values_list("terminal_id", flat=True)
    if organization_id:
        toilet_queryset = toilet_queryset.filter(management_id=organization_id)
    if toilet_type_id:
        toilet_queryset = toilet_queryset.filter(management_id=organization_id)
    in_clause = ""
    if organization_id or toilet_type_id:
        terminal_ids = json.dumps(list(toilet_queryset))
        in_clause = f"|> filter(fn: (r) => contains(value: r.terminal_id, set: {terminal_ids}))"

    query_api = influxdb_client.query_api()
    flux = (
        f'from(bucket: "{const.INFLUXDB_BUCKET}")'
        f"|> range(start: {start_time.isoformat()}, stop: {end_time.isoformat()})"
        '|> filter(fn: (r) => r._measurement == "toilet_seat" and exists r.installation_location'
        ' and (r.installation_location == "MEN" or r.installation_location == "WOMEN" or r.installation_location == "GENDERLESS"))'  # noqa
        f"{in_clause}"
        '|> group(columns: ["_measurement", "terminal_id", "installation_location", "seat_serial"])'
        "|> difference(nonNegative: true)"
        '|> group(columns: ["_measurement", "terminal_id", "installation_location"])|> sum()'
        '|> pivot(columnKey: ["installation_location"], rowKey: ["terminal_id"], valueColumn: "_value")'
    )
    if terminal_id:
        flux += f'|> filter(fn: (r) => r.terminal_id == "{terminal_id}")'
    flux += '|> group()|> sort(columns: ["_terminal_id"])'

    # 统计总条数
    count = flux_list_count(flux, query_api)
    # 查询列表
    flux += f"|> limit(n: {limit}, offset: {offset})"
    logger.debug(flux)
    tables = query_api.query(flux)
    models: List[ToiletSeatStatistics] = flux_tables_to_models(tables, ToiletSeatStatistics)
    # 补充公厕名、组织机构、公厕类型等信息
    toilets = Toilet.objects.filter(terminal_id__in={m.terminal_id for m in models}).select_related(
        "management", "toilet_type"
    )
    toilets_map = {t.terminal_id: t for t in toilets}

    results = []
    for model in models:
        toilet = toilets_map.get(model.terminal_id)
        toilet_name = toilet.name if toilet else None
        toilet_type = toilet.toilet_type.name if toilet and toilet.toilet_type else None
        organization_id = toilet.management.id if toilet and toilet.management else None
        organization_name = toilet.management.name if toilet and toilet.management else None
        results.append(
            ToiletSeatStatisticsOut(
                toilet_name=toilet_name,
                toilet_type=toilet_type,
                organization_id=organization_id,
                organization_name=organization_name,
                **model.dict(exclude_none=True),
            )
        )
    return {"count": count, "results": results}
