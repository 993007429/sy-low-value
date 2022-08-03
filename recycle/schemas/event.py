from ninja import ModelSchema
from pydantic import Field

from recycle.models import Event
from recycle.models.event import EventType


class EventOut(ModelSchema):
    type: EventType = Field(title="事件类型")

    class Config:
        model = Event
        model_fields = "__all__"
