import json
import logging
from datetime import datetime
from typing import List

from influxdb_client.client.write_api import SYNCHRONOUS
from ninja import Query, Router
from ninja.errors import HttpError

from app.models import Toilet
from app.models.sensors import Ammeter, Sensor
from app.schemas import Pagination
from app.schemas.ammeter import AmmeterIn, AmmeterOut, AmmeterStatistics, AmmeterStatisticsOut
from infra import const
from infra.authentication import AuthToken, TerminalAuth, terminal_auth
from infra.db.influxdb import flux_list, flux_list_count, flux_tables_to_models, influxdb_client

logger = logging.getLogger("influxdb.query")

router = Router(tags=["电表信息"])


@router.post("", response={201: None}, auth=terminal_auth)
def create_ammeter(request, ammeter_in: AmmeterIn):
    """上传电表传感器数据"""

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    toilet = request.auth
    ammeter = Ammeter(
        toilet_name=toilet.name,
        terminal_id=ammeter_in.terminal_id,
        sensor_id=ammeter_in.sensor_id,
        gather_time=ammeter_in.gather_time,
        kwh=ammeter_in.kwh,
    )
    data_point = ammeter.to_data_point()
    write_api.write(bucket=const.INFLUXDB_BUCKET, record=data_point)
    # 更新传感器最后通信时间
    Sensor.update_last_communication_time(ammeter_in.sensor_id, ammeter_in.gather_time)
    return 201


@router.get("", response=Pagination[AmmeterOut])
def get_ammeter(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str = None,
    sensor_id: str = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, le=100),
):
    """查询电表传感器数据上传记录"""
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")
    offset = (page - 1) * page_size
    limit = page_size
    # TODO: 参数化查询解决注入问题（参考air_quality）
    query_api = influxdb_client.query_api()
    flux = (
        f'from(bucket: "{const.INFLUXDB_BUCKET}")'
        f"|> range(start: {start_time.isoformat()}, stop: {end_time.isoformat()})"
        '|> filter(fn: (r) => r._measurement == "ammeter")'
        '|> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")'
    )
    if terminal_id:
        flux += f'|> filter(fn: (r) => r.terminal_id == "{terminal_id}")'
    if sensor_id:
        flux += f'|> filter(fn: (r) => r.sensor_id == "{sensor_id}")'
    flux += "|> group()"

    # 分页总条数
    count = flux_list_count(flux, query_api)
    # 分页列表
    flux = flux_list(flux, limit, offset)
    logger.debug(flux)
    tables = query_api.query(flux)
    ammeters = flux_tables_to_models(tables, Ammeter)
    return {"count": count, "results": ammeters}


@router.get("/statistics", response=Pagination[AmmeterStatisticsOut], auth=[AuthToken(), TerminalAuth()])
def get_ammeter_statistics(
    request,
    start_time: datetime,
    end_time: datetime,
    terminal_id: str = None,
    organization_id: int = None,
    toilet_type_id: int = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, le=100),
):
    """各个公厕用电量统计"""
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
        '|> filter(fn: (r) => r._measurement == "ammeter" and r._field == "kwh")'
        f"{in_clause}"
        '|> group(columns: ["_measurement", "terminal_id", "_field"])'
        "|> difference(nonNegative: true)"
        "|> sum()"
        '|> pivot(columnKey: ["_field"], rowKey: ["terminal_id"], valueColumn: "_value")'
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
    models: List[AmmeterStatistics] = flux_tables_to_models(tables, AmmeterStatistics)
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
            AmmeterStatisticsOut(
                terminal_id=model.terminal_id,
                toilet_name=toilet_name,
                toilet_type=toilet_type,
                organization_id=organization_id,
                organization_name=organization_name,
                kwh=model.kwh,
            )
        )

    return {"count": count, "results": results}
