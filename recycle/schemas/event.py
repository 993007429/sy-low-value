from ninja import ModelSchema

from recycle.models import Event


class EventOut(ModelSchema):
    class Config:
        model = Event
        model_fields = "__all__"
