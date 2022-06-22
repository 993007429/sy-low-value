from app.services.air_quality import AirQualityService
from app.services.passenger_volume import PassengerVolumeService
from app.services.toilet_seat_service import ToiletSeatService
from app.services.water_meter import WaterMeterService
from infra.db.influxdb import influxdb_client


def get_air_quality_service() -> AirQualityService:
    return AirQualityService(influxdb_client.query_api())


def get_water_meter_service() -> WaterMeterService:
    return WaterMeterService(influxdb_client.query_api())


def get_passenger_volume_service() -> PassengerVolumeService:
    return PassengerVolumeService(influxdb_client.query_api())


def get_toilet_seat_service() -> ToiletSeatService:
    return ToiletSeatService(influxdb_client.query_api())
