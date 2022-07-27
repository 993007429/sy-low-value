from django.conf import settings
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
        parser.add_argument(
            "-r",
            "--role",
            help="角色。默认区级",
        )

        parser.add_argument(
            "-c",
            "--region_code",
            help="区域编码",
        )

    def handle(
        self,
        username: str,
        password: str,
        role: str = PlatformManager.AREA,
        region_code: str = settings.REGION_CODE,
        *args,
        **options
    ):
        if not (username and password):
            self.stdout.write("请提供用户名和密码")
            return
        if not role:
            role = PlatformManager.AREA
        if role not in (PlatformManager.AREA, PlatformManager.STREET):
            self.stdout.write("无效的角色，可选AREA STREET")
            return
        create_platform_user(username, password, role, region_code)
        self.stdout.write("OK!")


def create_platform_user(username: str, password: str, role: str, region_code: str):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        PlatformManager.objects.create(user=user, role=role, region_id=region_code)
