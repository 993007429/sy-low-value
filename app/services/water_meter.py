import logging
from typing import List

from influxdb_client import QueryApi

from app.schemas.water_meter import WaterMeterRealtimeInfoOut
from infra import const
from infra.db.influxdb import flux_tables_to_models

logger = logging.getLogger("influxdb.query")


class WaterMeterService:
    def __init__(self, query_api: QueryApi):
        self.query_api = query_api

    def get_realtime_meter(self, terminal_id: str) -> WaterMeterRealtimeInfoOut:
        """获取指定公厕实时水表、电表数。因为电表、水表处理逻辑一样，这里把电表、水表放到一起了"""

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            '|> filter(fn: (r) => (r._measurement == "ammeter" or r._measurement == "water_meter")'
            f' and r.terminal_id == "{terminal_id}")'
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
        results: List[WaterMeterRealtimeInfoOut] = flux_tables_to_models(tables, WaterMeterRealtimeInfoOut)
        assert len(results) <= 1
        return results[0] if results else None

    def bulk_get_realtime_meter(self) -> List[WaterMeterRealtimeInfoOut]:
        """批量获取公厕实时水表、电表数。因为电表、水表处理逻辑一样，这里把电表、水表放到一起了"""

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            '|> filter(fn: (r) => r._measurement == "ammeter" or r._measurement == "water_meter")'
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
        results: List[WaterMeterRealtimeInfoOut] = flux_tables_to_models(tables, WaterMeterRealtimeInfoOut)
        return results
