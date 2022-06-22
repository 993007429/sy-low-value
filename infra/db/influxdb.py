import logging
from inspect import signature
from typing import List

from django.conf import settings
from influxdb_client import InfluxDBClient, QueryApi
from influxdb_client.client.flux_table import FluxTable

logger = logging.getLogger("influxdb.query")

influxdb_client = InfluxDBClient(
    url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG, debug=settings.DEBUG
)


def flux_tables_to_models(tables: List[FluxTable], cls_type: type):
    cls_fields = {field for field in signature(cls_type).parameters}
    models = []
    for table in tables:
        for record in table.records:
            kwargs = {attr: value for attr, value in record.values.items() if attr in cls_fields and value is not None}
            models.append(cls_type(**kwargs))
    return models


def flux_list_count(flux: str, query_api: QueryApi, params: dict = None):
    """给flux语句增加计算列表count的操作"""
    flux = flux + '|> count(column: "_measurement")'
    logger.debug(flux)
    tables = query_api.query(flux, params=params)
    if tables:
        assert len(tables) == 1, "确保你的flux查询调用了 group()"
        count = tables[0].records[0]["_measurement"]  # 列表总条数聚合，正常应该一个table,一个record
    else:
        count = 0
    return count


def flux_list(flux: str, limit: int, offset: int):
    """给flux查询语句增加按时间倒序排序，分页等操作"""

    flux += (
        '|> sort(columns: ["_time"], desc: true)'
        f"|> limit(n: {limit}, offset: {offset})"
        '|> rename(columns: {"_time": "gather_time"})'
    )
    return flux
