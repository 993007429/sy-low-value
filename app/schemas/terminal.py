from datetime import datetime

from ninja import Schema


class AppVersion(Schema):
    version_code: int
    version_name: str
    bluetooth_is_online: bool


class AppVersionIn(AppVersion):
    pass


class AppVersionOut(AppVersion):
    terminal_id: str
    created_at: datetime
    updated_at: datetime
