from django.core.management import BaseCommand
from django.db import transaction

from infra.authentication import User
from recycle.models import PlatformManager


class Command(BaseCommand):
    help = "create platform user"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--username",
            help="用户名",
        )
        parser.add_argument(
            "-p",
            "--password",
            help="密码",
        )

    def handle(self, username: str, password: str, *args, **options):
        if not (username and password):
            self.stdout.write("请提供用户名和密码")
            return
        create_platform_user(username, password)
        self.stdout.write("OK!")


def create_platform_user(username: str, password: str):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        PlatformManager.objects.create(
            user=user,
        )
