import logging
from typing import List

from influxdb_client import QueryApi

from app.schemas.toilet_seat import ToiletSeatRealtimeInfoOut
from infra import const
from infra.db.influxdb import flux_tables_to_models

logger = logging.getLogger("influxdb.query")


class ToiletSeatService:
    def __init__(self, query_api: QueryApi):
        self.query_api = query_api

    def get_realtime_toilet_seats(self, terminal_id: str) -> ToiletSeatRealtimeInfoOut:
        """获取指定公厕实时坑位占用情况"""

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            '|> filter(fn: (r) => r._measurement == "toilet_seat"'
            f' and r.terminal_id == "{terminal_id}"'
            ' and (r.installation_location == "MEN" or r.installation_location == "WOMEN" or r.installation_location == "GENDERLESS"))'  # noqa
            '|> group(columns:["sensor_id"])'
            '|> top(n: 1, columns: ["_time"])'
            '|> group(columns: ["_measurement", "terminal_id", "installation_location"])'
            "|> sum()"
            '|> pivot(columnKey: ["installation_location"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[ToiletSeatRealtimeInfoOut] = flux_tables_to_models(tables, ToiletSeatRealtimeInfoOut)
        assert len(results) <= 1
        return results[0] if results else None

    def bulk_get_realtime_toilet_seats(self) -> List[ToiletSeatRealtimeInfoOut]:
        """批量获取公厕实时坑位占用情况"""

        flux = (
            f'from(bucket: "{const.INFLUXDB_BUCKET}")'
            "|> range(start: -1d)"
            '|> filter(fn: (r) => r._measurement == "toilet_seat"'
            ' and (r.installation_location == "MEN" or r.installation_location == "WOMEN" or r.installation_location == "GENDERLESS"))'  # noqa
            '|> group(columns:["sensor_id"])'
            '|> top(n: 1, columns: ["_time"])'
            '|> group(columns: ["_measurement", "terminal_id", "installation_location"])'
            "|> sum()"
            '|> pivot(columnKey: ["installation_location"], rowKey: ["terminal_id"], valueColumn: "_value")'
        )
        logger.debug(flux)
        tables = self.query_api.query(flux)
        results: List[ToiletSeatRealtimeInfoOut] = flux_tables_to_models(tables, ToiletSeatRealtimeInfoOut)
        return results
