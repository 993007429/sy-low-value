from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "help text"

    def add_arguments(self, parser):
        parser.add_argument(
            "text",
            help="help text",
        )

    def handle(self, echo: str, *args, **options):
        self.stdout.write(echo)
