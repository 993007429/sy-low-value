import logging
from datetime import datetime
from typing import List

from influxdb_client.client.write_api import SYNCHRONOUS
from ninja import Query, Router

from infra import const
from infra.db.influxdb import influxdb_client
from recycle.models.track import Track
from recycle.schemas.track import TrackIn, TrackOut

router = Router(tags=["车辆轨迹"])
logger = logging.getLogger("influxdb.query")


# TODO: 增加认证
@router.post("", response={201: None}, auth=None)
def create_track(request, data: TrackIn):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    track = Track(
        plate_number=data.plate_number,
        tracked_at=data.tracked_at,
        phone=data.phone,
        longitude=data.longitude,
        latitude=data.latitude,
        altitude=data.altitude,
        speed=data.speed,
        direction=data.direction,
    )
    data_point = track.to_data_point()
    write_api.write(bucket=const.INFLUXDB_BUCKET, record=data_point)


# @router.get("", response=List[TrackOut])
# def list_tracks(
#     request,
#     plate_number: str = Query(..., description="车牌号"),
#     start_time: datetime = Query(..., description="开始时间"),
#     end_time: datetime = Query(..., description="结束时间"),
# ):
#     # TODO: 更换真实数据, 限制时间范围
#     if start_time >= end_time:
#         raise HttpError(400, "开始时间应小于结束时间")
#
#     flux_params = {
#         "start": start_time,
#         "stop": end_time,
#         "plate_number": plate_number,
#     }
#     query_api = influxdb_client.query_api()
#     flux = (
#         f'from(bucket: "{const.INFLUXDB_BUCKET}")'
#         "|> range(start: start, stop: stop)"
#         '|> filter(fn: (r) => r._measurement == "track")'
#         '|> pivot(rowKey: ["_time"], columnKey: ["_field",], valueColumn: "_value")'
#     )
#     if plate_number:
#         flux += "|> filter(fn: (r) => r.terminal_id == terminal_id)"
#     flux += '|> group()|> sort(columns: ["_time"], desc: true)'
#     logger.debug(flux)
#
#     tables = query_api.query(flux, params=flux_params)
#     tracks = flux_tables_to_models(tables, TrackOut)
#     return tracks


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
