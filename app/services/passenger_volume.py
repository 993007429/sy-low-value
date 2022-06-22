import logging
from datetime import datetime, timedelta
from typing import List

from influxdb_client import QueryApi

from app.schemas.passenger_volume import (
    BatchPassengerVolumeLastHourMean,
    PassengerVolumeRealtimeInfoOut,
    PassengerVolumeWindowMean,
)
from infra import const
from infra.const import PeriodEnum
from infra.db.influxdb import flux_tables_to_models

logger = logging.getLogger("influxdb.query")


class PassengerVolumeService:
    def __init__(self, query_api: QueryApi):
        self.query_api = query_api

    def get_realtime_volume(self, terminal_id: str) -> PassengerVolumeRealtimeInfoOut:
        """获取指定公厕实时客流量。"""
        # TODO: 参数化查询解决注入问题（参考air_quality）

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            f'|> filter(fn: (r) => r._measurement == "passenger_volume" and r.terminal_id == "{terminal_id}")'
            '|> group(columns: ["_measurement", "_field", "sensor_id"])'
            '|> sort(columns: ["_time"], desc: true)'
            "|> limit(n: 1)"
            '|> group(columns: ["_measurement", "_field", "terminal_id"])'
            "|> sum()"
            "|> group()"
            '|> pivot(columnKey: ["_field"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[PassengerVolumeRealtimeInfoOut] = flux_tables_to_models(tables, PassengerVolumeRealtimeInfoOut)
        assert len(results) <= 1
        return results[0] if results else None

    def bulk_get_realtime_volume(self) -> List[PassengerVolumeRealtimeInfoOut]:
        """批量获取公厕实时客流量。"""
        # TODO: 参数化查询解决注入问题（参考air_quality）

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            f'|> filter(fn: (r) => r._measurement == "passenger_volume")'
            '|> group(columns: ["_measurement", "_field", "sensor_id"])'
            '|> sort(columns: ["_time"], desc: true)'
            "|> limit(n: 1)"
            '|> group(columns: ["_measurement", "_field", "terminal_id"])'
            "|> sum()"
            "|> group()"
            '|> pivot(columnKey: ["_field"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[PassengerVolumeRealtimeInfoOut] = flux_tables_to_models(tables, PassengerVolumeRealtimeInfoOut)
        return results

    def aggregate_window_incremental(
        self, terminal_id: str, start_time: datetime, stop_time: datetime, period: PeriodEnum
    ) -> List[PassengerVolumeWindowMean]:
        start_time -= timedelta(hours=1)  # 为了包括左侧临界值
        # TODO: 参数化查询解决注入问题（参考air_quality）

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            f"|> range(start: {start_time.isoformat()}, stop: {stop_time.isoformat()})"
            f'|> filter(fn: (r) => r._measurement == "passenger_volume" and r.terminal_id == "{terminal_id}")'
            '|> group(columns: ["_measurement", "_field", "terminal_id", "sensor_id"])'
            f"|> aggregateWindow(every: {period.value}, fn: last, createEmpty: true)"
            "|> difference()"
            '|> group(columns: ["_measurement", "_field", "terminal_id","_time"])'
            "|> sum()"
            '|> pivot(columnKey: ["_field"], rowKey: ["_time"], valueColumn: "_value")'
            "|> group()"
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[PassengerVolumeWindowMean] = flux_tables_to_models(tables, PassengerVolumeWindowMean)
        return results

    def batch_incremental_last_hour(self, stop_time: datetime) -> List[BatchPassengerVolumeLastHourMean]:
        start_time = stop_time - timedelta(hours=1)
        # TODO: 参数化查询解决注入问题（参考air_quality）

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            f"|> range(start: {start_time.isoformat()}, stop: {stop_time.isoformat()})"
            f'|> filter(fn: (r) => r._measurement == "passenger_volume")'
            '|> group(columns: ["_measurement", "_field", "terminal_id", "sensor_id"])'
            "|> difference()"
            '|> group(columns: ["terminal_id"])'
            "|> sum()"
            "|> group()"
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[BatchPassengerVolumeLastHourMean] = flux_tables_to_models(
            tables, BatchPassengerVolumeLastHourMean
        )
        return results
