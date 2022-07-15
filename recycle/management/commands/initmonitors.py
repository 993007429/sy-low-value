import csv

from django.core.management import BaseCommand

from recycle.models import Monitor


class Command(BaseCommand):
    help = "初始化设施监控"

    def handle(self, *args, **options):
        initial_monitor()


def initial_monitor():
    monitors = []
    with open("recycle/migrations/monitors.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            monitors.append(
                Monitor(
                    serial=row["serial"],
                    code=row["code"],
                    site_type=row["site_type"],
                    site_name=row["site_name"],
                    station_id=row["station"],
                )
            )
    Monitor.objects.bulk_create(monitors, ignore_conflicts=True)
