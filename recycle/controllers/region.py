from typing import List

from django.conf import settings
from ninja import Router

from recycle.models import Region, RegionGrade
from recycle.schemas.region import RegionOut

router = Router(tags=["区域"])


@router.get("/area", response=List[RegionOut])
def list_areas(request):
    """区列表"""

    regions = Region.objects.filter(grade=RegionGrade.AREA)
    return regions


@router.get("/street", response=List[RegionOut])
def list_streets(request):
    """街道列表"""

    regions = Region.objects.filter(parent__code=settings.REGION_CODE, grade=RegionGrade.STREET).order_by("code")
    return regions
