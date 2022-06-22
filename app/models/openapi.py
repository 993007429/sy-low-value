import shortuuid
from django.db import models

from infra.db.models import BaseModel


class Agent(BaseModel):
    """信任的三方系统"""

    agent_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True)
    secret = models.CharField(max_length=255, unique=True)
    authorizer = models.ForeignKey("User", db_constraint=False, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(BaseModel):
    """Ticket 用于从信任的三方系统免密登录智慧公厕系统"""

    ticket = models.CharField(max_length=255, unique=True)
    agent = models.ForeignKey(Agent, db_constraint=False, on_delete=models.CASCADE)
    used = models.BooleanField("是否用过", help_text="只能用一次，用过无效", default=False)
    expired_at = models.DateTimeField()

    def __str__(self):
        return self.ticket


def generate_ticket() -> str:
    return shortuuid.uuid()
