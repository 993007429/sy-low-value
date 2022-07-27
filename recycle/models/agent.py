import time

from django.core.signing import Signer
from django.db import models

from infra.db.models import BaseModel


class Agent(BaseModel):
    """信任的三方系统"""

    agent_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True)
    secret = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def get_token_for_agent(agent_id: str):
    signer = Signer()
    payload = {"agent": agent_id, "ts": int(time.time())}
    return signer.sign_object(payload)
