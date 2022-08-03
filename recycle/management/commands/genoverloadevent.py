from django.core.management import BaseCommand

from recycle.models import Event, InboundRecord, Vehicle
from recycle.models.event import EventType


class Command(BaseCommand):
    help = "读取进站数据、生成超重预警事件"

    def handle(self, *args, **options):
        counts = 0
        for inbound in InboundRecord.objects.iterator():
            vehicle = Vehicle.objects.filter(plate_number=inbound.plate_number).first()
            if vehicle and inbound.net_weight > vehicle.load * 1000:
                Event.objects.create(
                    plate_number=inbound.plate_number,
                    started_at=inbound.net_weight_time,
                    ended_at=inbound.net_weight_time,
                    type=EventType.OVERLOAD,
                )
                counts += 1
        self.stdout.write(f"OK! {counts} events")
