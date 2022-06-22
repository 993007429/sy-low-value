import logging
from datetime import datetime, timedelta
from typing import List

from influxdb_client import QueryApi

from app.schemas.air_quality import AirQualityRealtimeInfoOut, AirQualityWindowMean, BatchAirQualityWindowMean
from infra import const
from infra.const import PeriodEnum
from infra.db.influxdb import flux_tables_to_models

logger = logging.getLogger("influxdb.query")


class AirQualityService:
    def __init__(self, query_api: QueryApi):
        self.query_api = query_api

    def get_realtime_air_quality(self, terminal_id: str) -> AirQualityRealtimeInfoOut:
        """获取指定公厕实时空气质量, 包括硫化氢和氨气"""

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            '|> filter(fn: (r) => (r._measurement == "air_quality" or r._measurement == "h2s" or r._measurement == "nh3")'  # noqa
            f' and r.terminal_id == "{terminal_id}" and (r.installation_location == "MEN" or r.installation_location == "WOMEN"))'  # noqa
            '|> group(columns: ["_measurement", "terminal_id", "installation_location", "_field"])'
            '|> sort(columns: ["_time"], desc: true)'
            "|> limit(n: 1)"
            "|> toFloat()"
            "|> group()"
            '|> pivot(columnKey: ["_field", "installation_location"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[AirQualityRealtimeInfoOut] = flux_tables_to_models(tables, AirQualityRealtimeInfoOut)
        assert len(results) <= 1
        return results[0] if results else None

    def bulk_get_realtime_air_quality(self) -> List[AirQualityRealtimeInfoOut]:
        """批量获取指定公厕实时空气质量, 包括硫化氢和氨气"""

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -30m)"
            '|> filter(fn: (r) => (r._measurement == "air_quality" or r._measurement == "h2s" or r._measurement == "nh3")'  # noqa
            f' and (r.installation_location == "MEN" or r.installation_location == "WOMEN"))'  # noqa
            '|> group(columns: ["_measurement", "terminal_id", "installation_location", "_field"])'
            '|> sort(columns: ["_time"], desc: true)'
            "|> limit(n: 1)"
            "|> toFloat()"
            "|> group()"
            '|> pivot(columnKey: ["_field", "installation_location"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[AirQualityRealtimeInfoOut] = flux_tables_to_models(tables, AirQualityRealtimeInfoOut)
        return results

    def aggregate_window_mean(
        self, terminal_id: str, start_time: datetime, stop_time: datetime, period: PeriodEnum
    ) -> List[AirQualityWindowMean]:
        flux_params = {
            "start": start_time,
            "stop": stop_time,
            "terminal_id": terminal_id,
        }
        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: start, stop: stop)"
            '|> filter(fn: (r) => r._measurement == "air_quality" or r._measurement == "h2s" or r._measurement == "nh3")'  # noqa
            "|> filter(fn: (r) => r.terminal_id == terminal_id)"
            "|> toFloat()"
            '|> group(columns: ["terminal_id", "_measurement", "_field"])'
            f"|> aggregateWindow(every: {period.value}, fn: mean, createEmpty: true)"
            '|> group(columns: ["terminal_id"])'
            '|> pivot(columnKey: ["_field"], rowKey: ["_time"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux, params=flux_params)
        results: List[AirQualityWindowMean] = flux_tables_to_models(tables, AirQualityWindowMean)
        return results

    def batch_mean_last_hour(self, stop_time: datetime) -> List[BatchAirQualityWindowMean]:
        start_time = stop_time - timedelta(hours=1)
        flux_params = {
            "start": start_time,
            "stop": stop_time,
        }
        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: start, stop: stop)"
            '|> filter(fn: (r) => r._measurement == "air_quality" or r._measurement == "h2s" or r._measurement == "nh3")'  # noqa
            "|> toFloat()"
            '|> group(columns: ["terminal_id", "_measurement", "_field"])'
            "|> mean()"
            "|> group()"
            '|> pivot(columnKey: ["_field"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux, params=flux_params)
        results: List[BatchAirQualityWindowMean] = flux_tables_to_models(tables, BatchAirQualityWindowMean)
        return results
