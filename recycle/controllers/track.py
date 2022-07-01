from ninja import Router

from recycle.schemas.track import TrackIn

router = Router(tags=["车辆轨迹"])


@router.post("", response={201: None}, auth=None)
def create_track(request, data: TrackIn):
    print(data)
