import csv

from django.core.management import BaseCommand

from recycle.models import RegionScope


class Command(BaseCommand):
    help = "初始化系统区域范围"

    def handle(self, *args, **options):
        initial_region_scope()


def initial_region_scope():
    region_scopes = []
    with open("recycle/migrations/region_scopes.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            region_scopes.append(
                RegionScope(
                    code=row["code"],
                    name=row["name"],
                    lon_lat=row["lon_lat"],
                    lat_center=row["lat_center"],
                    lon_center=row["lon_center"],
                    is_null=row["is_null"],
                )
            )
    RegionScope.objects.bulk_create(region_scopes, ignore_conflicts=True)
