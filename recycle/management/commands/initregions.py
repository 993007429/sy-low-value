import csv

from django.core.management import BaseCommand

from recycle.models import Region
from recycle.models.region import RegionGrade


class Command(BaseCommand):
    help = "初始化系统区域"

    def handle(self, *args, **options):
        initial_region()


def initial_region():
    regions = []
    with open("recycle/migrations/regions.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            regions.append(Region(code=row["code"], name=row["name"], grade=row["grade"]))
    Region.objects.bulk_create(regions, ignore_conflicts=True)
    areas = Region.objects.filter(grade=RegionGrade.AREA)
    for area in areas:
        area_code_prefix = area.code[:6]
        Region.objects.filter(grade=RegionGrade.STREET, code__startswith=area_code_prefix).update(parent=area)

    streets = Region.objects.filter(grade=RegionGrade.STREET)
    for street in streets:
        street_code_prefix = street.code[:9]
        Region.objects.filter(grade=RegionGrade.COMMUNITY, code__startswith=street_code_prefix).update(parent=street)
