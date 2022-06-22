import json
import logging
from datetime import datetime
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from influxdb_client.client.write_api import SYNCHRONOUS
from ninja import Query, Router
from ninja.errors import HttpError

from app.depends import get_air_quality_service
from app.models import Toilet
from app.models.sensors import AirQuality, Sensor
from app.schemas import Pagination
from app.schemas.air_quality import (
    AirQualityIn,
    AirQualityOut,
    AirQualityStatistics,
    AirQualityStatisticsOut,
    AirQualityWindowMeanOut,
    BatchAirQualityWindowMeanOut,
)
from infra import const
from infra.authentication import terminal_auth
from infra.const import PeriodEnum
from infra.db.influxdb import flux_list, flux_list_count, flux_tables_to_models, influxdb_client
from infra.utils import now_tz_aware

router = Router(tags=["空气质量"])

logger = logging.getLogger("influxdb.query")


@router.post("", response={201: None}, auth=terminal_auth)
def create_air_quality(request, air_quality_in: AirQualityIn):
    """空气质量传感器数据上传"""

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    toilet = request.auth
    sensor = Sensor.objects.filter(sensor_id=air_quality_in.sensor_id).first()
    air_quality = AirQuality(
        toilet_name=toilet.name,
        terminal_id=air_quality_in.terminal_id,
        sensor_id=air_quality_in.sensor_id,
        installation_location=sensor.installation_location if sensor else None,
        gather_time=air_quality_in.gather_time,
        temperature=air_quality_in.temperature,
        humidity=air_quality_in.humidity,
        pm2_5=air_quality_in.pm2_5,
        pm10=air_quality_in.pm10,
        co2=air_quality_in.co2,
    )
    data_point = air_quality.to_data_point()
    write_api.write(bucket=const.INFLUXDB_BUCKET, record=data_point)
    # 更新传感器最后通信时间
    Sensor.update_last_communication_time(air_quality.sensor_id, air_quality.gather_time)
    return 201


@router.get("", response=Pagination[AirQualityOut])
def get_air_quality(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str = None,
    sensor_id: str = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """查询空气质量上传记录"""
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")

    offset = (page - 1) * page_size
    limit = page_size
    flux_params = {
        "start": start_time,
        "stop": end_time,
        "terminal_id": terminal_id,
        "sensor_id": sensor_id,
    }

    query_api = influxdb_client.query_api()
    flux = (
        f'from(bucket: "{const.INFLUXDB_BUCKET}")'
        "|> range(start: start, stop: stop)"
        '|> filter(fn: (r) => r._measurement == "air_quality")'
        '|> pivot(rowKey: ["_time"], columnKey: ["_field",], valueColumn: "_value")'
    )
    if terminal_id:
        flux += "|> filter(fn: (r) => r.terminal_id == terminal_id)"
    if sensor_id:
        flux += "|> filter(fn: (r) => r.sensor_id == sensor_id)"
    flux += "|> group()"

    # 统计总条数
    count = flux_list_count(flux, query_api, flux_params)
    # 查询列表
    flux = flux_list(flux, limit, offset)
    logger.debug(flux)
    tables = query_api.query(flux, params=flux_params)
    air_qualities = flux_tables_to_models(tables, AirQuality)
    return {"count": count, "results": air_qualities}


@router.get("/statistics", response=Pagination[AirQualityStatisticsOut])
def get_air_quality_statistics(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str = None,
    organization_id: int = None,
    toilet_type_id: int = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, le=100),
):
    """查询空气质量上传记录"""
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")

    offset = (page - 1) * page_size
    limit = page_size
    flux_params = {
        "start": start_time,
        "stop": end_time,
        "terminal_id": terminal_id,
    }

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
        "|> range(start: start, stop: stop)"
        '|> filter(fn: (r) => r._measurement == "air_quality")'
        '|> filter(fn: (r) => exists r.installation_location and (r.installation_location == "MEN" or r.installation_location == "WOMEN"))'  # noqa
        f"{in_clause}"
        '|> group(columns: ["_measurement", "terminal_id", "installation_location", "_field"])'
        "|> mean()"
        '|> pivot(rowKey: ["terminal_id"], columnKey: ["_field", "installation_location"], valueColumn: "_value")'
    )
    if terminal_id:
        flux += "|> filter(fn: (r) => r.terminal_id == terminal_id)"
    flux += '|> group()|> sort(columns: ["_terminal_id"])'

    # 统计总条数
    count = flux_list_count(flux, query_api, flux_params)
    # 查询列表
    flux += f"|> limit(n: {limit}, offset: {offset})"
    logger.debug(flux)
    tables = query_api.query(flux, params=flux_params)
    models: List[AirQualityStatistics] = flux_tables_to_models(tables, AirQualityStatistics)
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
            AirQualityStatisticsOut(
                toilet_name=toilet_name,
                toilet_type=toilet_type,
                organization_id=organization_id,
                organization_name=organization_name,
                **model.dict(exclude_none=True),
            )
        )
    return {"count": count, "results": results}


@router.get("/aggregation-window/mean", response=AirQualityWindowMeanOut)
def aggregate_window(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str,
    period: PeriodEnum = PeriodEnum.EVERY_HOUR,
):
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")
    try:
        toilet = Toilet.objects.get(terminal_id=terminal_id)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕不存在")
    air_quality_service = get_air_quality_service()
    agg = air_quality_service.aggregate_window_mean(terminal_id, start_time, end_time, period)
    data = AirQualityWindowMeanOut(
        terminal_id=toilet.terminal_id,
        toilet_name=toilet.name,
        data=agg,
    )
    return data


@router.get("/batch/mean-last-hour", response=List[BatchAirQualityWindowMeanOut])
def batch_mean_last_hour(request, stop_time: datetime = None):
    """所有公厕最近一小时平均空气质量"""
    stop_time = stop_time or now_tz_aware()
    air_quality_service = get_air_quality_service()
    aggregations = air_quality_service.batch_mean_last_hour(stop_time)

    toilets_dict = {t.terminal_id: t for t in Toilet.objects.all()}
    data = []
    for agg in aggregations:
        toilet = toilets_dict.get(agg.terminal_id)
        item = BatchAirQualityWindowMeanOut(
            **agg.dict(),
            toilet_name=toilet.name if toilet else "",
            code=toilet.code if toilet else "",
            time=stop_time,
        )
        data.append(item)

    return data
