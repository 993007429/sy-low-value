import logging
from datetime import datetime
from typing import List

from ninja import Query, Router

from recycle.schemas.track import TrackIn, TrackOut

router = Router(tags=["车辆轨迹"])
logger = logging.getLogger("influxdb.query")


@router.post("", response={201: None}, auth=None)
def create_track(request, data: TrackIn):
    print(data)


# def create_track2(request, data: TrackIn):
#     """空气质量传感器数据上传"""
#
#     write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
#     toilet = request.auth
#     sensor = Sensor.objects.filter(sensor_id=air_quality_in.sensor_id).first()
#     air_quality = AirQuality(
#         toilet_name=toilet.name,
#         terminal_id=air_quality_in.terminal_id,
#         sensor_id=air_quality_in.sensor_id,
#         installation_location=sensor.installation_location if sensor else None,
#         gather_time=air_quality_in.gather_time,
#         temperature=air_quality_in.temperature,
#         humidity=air_quality_in.humidity,
#         pm2_5=air_quality_in.pm2_5,
#         pm10=air_quality_in.pm10,
#         co2=air_quality_in.co2,
#     )
#     data_point = air_quality.to_data_point()
#     write_api.write(bucket=const.INFLUXDB_BUCKET, record=data_point)
#     # 更新传感器最后通信时间
#     Sensor.update_last_communication_time(air_quality.sensor_id, air_quality.gather_time)
#     return 201


@router.get("", response=List[TrackOut])
def list_tracks(
    request,
    plate_number: str = Query(..., description="车牌号"),
    start_time: datetime = Query(..., description="开始时间"),
    end_time: datetime = Query(..., description="结束时间"),
):
    # TODO: 更换真实数据, 限制时间范围
    tracks = [
        TrackOut(plate_number="京A1234", tracked_at=0, longitude=116.466522, latitude=39.893098),
        TrackOut(plate_number="京A1234", tracked_at=0, longitude=116.482229, latitude=39.892966),
        TrackOut(plate_number="京A1234", tracked_at=0, longitude=116.496305, latitude=39.888027),
        TrackOut(plate_number="京A1234", tracked_at=0, longitude=116.488409, latitude=39.882363),
        TrackOut(plate_number="京A1234", tracked_at=0, longitude=116.478795, latitude=39.885261),
        TrackOut(plate_number="京A1234", tracked_at=0, longitude=116.478795, latitude=39.890332),
    ]
    return tracks
