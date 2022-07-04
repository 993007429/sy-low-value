import logging
from datetime import datetime
from typing import List

from influxdb_client.client.write_api import SYNCHRONOUS
from ninja import Query, Router
from ninja.errors import HttpError

from infra import const
from infra.db.influxdb import flux_tables_to_models, influxdb_client
from recycle.models.track import LatestTrack, Track
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
    # 更新车辆最新位置
    LatestTrack.objects.update_or_create(
        defaults={
            "longitude": data.longitude,
            "latitude": data.latitude,
            "altitude": data.altitude,
            "speed": data.speed,
            "direction": data.direction,
        },
        plate_number=data.plate_number,
    )


@router.get("", response=List[TrackOut])
def list_tracks(
    request,
    plate_number: str = Query(..., description="车牌号"),
    start_time: datetime = Query(..., description="开始时间"),
    end_time: datetime = Query(..., description="结束时间"),
):
    if start_time >= end_time:
        raise HttpError(400, "开始时间应小于结束时间")

    flux_params = {
        "start": start_time,
        "stop": end_time,
        "plate_number": plate_number,
    }
    query_api = influxdb_client.query_api()
    flux = (
        f'from(bucket: "{const.INFLUXDB_BUCKET}")'
        "|> range(start: start, stop: stop)"
        '|> filter(fn: (r) => r._measurement == "track")'
        '|> pivot(rowKey: ["_time"], columnKey: ["_field",], valueColumn: "_value")'
    )
    if plate_number:
        flux += "|> filter(fn: (r) => r.plate_number == plate_number)"
    flux += '|> group()|> sort(columns: ["_time"])'
    logger.debug(flux)

    tables = query_api.query(flux, params=flux_params)
    tracks = flux_tables_to_models(tables, TrackOut)
    return tracks
