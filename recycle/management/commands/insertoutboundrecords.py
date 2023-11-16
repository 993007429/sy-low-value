import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from infra.utils import uuid1
from recycle.models import OutboundRecord


class Command(BaseCommand):
    help = "导入出场记录"

    def add_arguments(self, parser):

        parser.add_argument(
            "-f",
            "--filename",
            help="文件",
        )

    def handle(self, filename: str, *args, **options):

        csvs = os.listdir(str(settings.BASE_DIR.parent) + "/recycle/migrations")

        if not filename:
            self.stdout.write("请提供文件")
            return

        if filename not in csvs:
            self.stdout.write("提供的文件不存在")
            return

        insert_outbound_records(filename)


def insert_outbound_records(filename):

    csv_path = os.path.join(settings.BASE_DIR.parent, "recycle/migrations", filename)
    outbound_records = []

    with open(csv_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            outbound_records.append(
                OutboundRecord(
                    tare_weight_time=row["tare_weight_time"],
                    gross_weight_time=row["gross_weight_time"],
                    net_weight_time=row["net_weight_time"],
                    station_id=row["station_id"],
                    weigher=row["weigher"],
                    plate_number=row["plate_number"],
                    driver=row["driver"],
                    carrier_name=row["carrier_name"],
                    recyclables_type=row["recyclables_type"],
                    category=row["category"],
                    tare_weight=row["tare_weight"] if row["tare_weight"] != '' else 0,
                    gross_weight=row["gross_weight"] if row["gross_weight"] != '' else 0,
                    net_weight=row["net_weight"] if row["net_weight"] != '' else 0,
                    plate_number_photo_out=row["plate_number_photo_out"] if row["plate_number_photo_out"] != '' else None,
                    vehicle_head_photo_out=row["vehicle_head_photo_out"] if row["vehicle_head_photo_out"] != '' else None,
                    vehicle_roof_photo_out=row["vehicle_roof_photo_out"] if row["vehicle_roof_photo_out"] != '' else None,
                    place_to_go=row["place_to_go"],
                    uuid=uuid1(),
                )
            )

    try:
        OutboundRecord.objects.bulk_create(outbound_records, ignore_conflicts=True)
    except Exception as e:
        print(f"数据更新失败: {e}")
    else:
        print("数据更新成功")
